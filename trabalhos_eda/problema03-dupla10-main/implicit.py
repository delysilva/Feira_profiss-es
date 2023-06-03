import Vector, Queue
import pyglet

class RectNode:
    @staticmethod   
    def midpoint(point1: Vector.Point,
                point2: Vector.Point, 
                to_int = True):
        assert (point1.dimension == 2) and (point2.dimension == 2)
        if to_int:
            return Vector.Point((point1[0] + point2[0]) // 2, (point1[1] + point2[1]) // 2)
        else:
            return Vector.Point((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)
        
    def center(self) -> Vector.Point:
        return RectNode.midpoint(self.bottom_left, self.top_right)

    def __init__(self, 
                bottom_left: Vector.Point,
                top_right: Vector.Point,
                depth: int):
        self.bottom_left = bottom_left
        self.top_right = top_right
        self.depth = depth
        self.subrects = Vector.StaticVector(4)
        for i in range(4):
            self.subrects.append(None)
    
    def __repr__(self) -> str:
        return f"Rect({self.bottom_left[0]}, {self.bottom_left[1]}, {self.top_right[0]}, {self.top_right[1]})"

    def width(self):
        return self.top_right[0] - self.bottom_left[0]

    def height(self):
        return self.top_right[1] - self.bottom_left[1]

    def make_subrects(self):
        """
        Note: not recursive (only immediate subrects)
        """
        # FIXME are those "if not degenerate etc" necessary?
        x0, y0, x1, y1 = self.bottom_left[0], self.bottom_left[1], self.top_right[0], self.top_right[1]
        
        if ((x1 - x0) > 1 or (y1 - y0) > 1): # not a single pixel
            # bottom left: 
            p1 = Vector.Point(x0, y0)
            p2 = Vector.Point((x0 + x1)//2, (y0 + y1)//2 )
            self.subrects[0] = RectNode(p1, p2, self.depth + 1)
            # bottom right:
            p1 = Vector.Point((x0 + x1)//2, y0)
            p2 = Vector.Point(x1, (y0 + y1)//2)
            self.subrects[1] = RectNode(p1, p2, self.depth + 1)
            # top left
            p1 = Vector.Point(x0, (y0 + y1)//2)
            p2 = Vector.Point((x0 + x1)//2, y1)
            self.subrects[2] = RectNode(p1, p2, self.depth + 1)
            # top right
            p1 = Vector.Point((x0 + x1)//2, (y0 + y1)//2)
            p2 = Vector.Point(x1, y1)
            self.subrects[3] = RectNode(p1, p2, self.depth + 1)

            
class QuadTree:
    def __init__(self,
                width: int,
                height: int,
                max_depth: int):
        self.max_depth = max_depth
        self.root = RectNode(Vector.Point(0, 0), # bottom_left
                            Vector.Point(width, height), # top_right
                            0) # depth
        self.rect_queue = Queue.Queue()
        self.rect_queue.queue(self.root)

    def build_tree(self):
        # builds queue from the current state to the nodes on depth = max_depth 
        while (not self.rect_queue.is_empty()):
            rect = self.rect_queue.get_front().get_val() # Queue Node is wrapper from data
            if (rect.depth >= self.max_depth): 
                break
            else:
                self.rect_queue.dequeue()
                rect.make_subrects()
                for r in rect.subrects:
                    if r is not None:
                        self.rect_queue.queue(r)
    
    def get_nodes_at_depth(self, depth: int) -> Queue.Queue:
        waiting_nodes = Queue.Queue()
        waiting_nodes.queue(self.root)
        while (waiting_nodes.get_front().get_val().depth < depth):
            rect = waiting_nodes.get_front().get_val()
            waiting_nodes.dequeue()
            for i in range(4):
                if (rect.subrects[i] is not None):
                    waiting_nodes.queue(rect.subrects[i])
        return waiting_nodes
    
    def make_batch_curve(self, f, root_color, depth):
        assert depth >= 2
        self.shapeList = Vector.DynamicVector()
        self.batch = pyglet.graphics.Batch()
        f_point = lambda p: f(p[0], p[1]) 
        waiting_nodes = self.get_nodes_at_depth(2)

        while (not waiting_nodes.is_empty()):
            rect = waiting_nodes.get_front().get_val() 
            waiting_nodes.dequeue()
            top_left = Vector.Point(rect.bottom_left[0], rect.top_right[1])
            bottom_right = Vector.Point(rect.top_right[0], rect.bottom_left[1])
            if (rect.depth < min(self.max_depth, depth)):
                if (f_point(top_left) > 0 and f_point(rect.top_right) > 0 and 
                    f_point(rect.bottom_left) > 0 and f_point(bottom_right) > 0):
                    continue
                elif (f_point(top_left) < 0 and f_point(rect.top_right) < 0 and 
                    f_point(rect.bottom_left) < 0 and f_point(bottom_right) < 0):
                    continue
                else:
                    for i in range(4):
                        if (rect.subrects[i] is not None):
                            waiting_nodes.queue(rect.subrects[i])
            else:
                self.shapeList.append(pyglet.shapes.Rectangle(rect.bottom_left[0],
                                                        rect.bottom_left[1],
                                                        rect.width(),
                                                        rect.height(),
                                                        root_color, 
                                                        self.batch
                                                        )
                                    )
    
    def make_batch_colored(self,
                            f, 
                            positive_color,
                            negative_color,
                            border_color,
                            depth: int):
        assert depth >= 2
        self.shapeList = Vector.DynamicVector()
        self.batch = pyglet.graphics.Batch()
        f_point = lambda p: f(p[0], p[1]) 
        waiting_nodes = self.get_nodes_at_depth(2)

        while (not waiting_nodes.is_empty()):
            rect = waiting_nodes.get_front().get_val() 
            waiting_nodes.dequeue()
            top_left = Vector.Point(rect.bottom_left[0], rect.top_right[1])
            bottom_right = Vector.Point(rect.top_right[0], rect.bottom_left[1])
            if (rect.depth < min(self.max_depth, depth)):
                if (f_point(top_left) > 0 and f_point(rect.top_right) > 0 and 
                    f_point(rect.bottom_left) > 0 and f_point(bottom_right) > 0):
                    self.shapeList.append(pyglet.shapes.Rectangle(rect.bottom_left[0],
                                            rect.bottom_left[1],
                                            rect.width(),
                                            rect.height(),
                                            positive_color, 
                                            self.batch)
                                        )
                elif (f_point(top_left) < 0 and f_point(rect.top_right) < 0 and 
                    f_point(rect.bottom_left) < 0 and f_point(bottom_right) < 0):
                    self.shapeList.append(pyglet.shapes.Rectangle(rect.bottom_left[0],
                                            rect.bottom_left[1],
                                            rect.width(),
                                            rect.height(),
                                            negative_color, 
                                            self.batch)
                                        )
                else:
                    for i in range(4):
                        if (rect.subrects[i] is not None):
                            waiting_nodes.queue(rect.subrects[i])
            else:
                self.shapeList.append(pyglet.shapes.Rectangle(rect.bottom_left[0],
                                        rect.bottom_left[1],
                                        rect.width(),
                                        rect.height(),
                                        border_color, 
                                        self.batch)
                                    )
        
    def make_batch_border(self, 
                            f, 
                            border_width: int, 
                            border_color: tuple, 
                            inside_color: tuple, 
                            depth: int):
        assert depth >= 2
        self.shapeList = Vector.DynamicVector()
        self.batch = pyglet.graphics.Batch()
        f_point = lambda p: f(p[0], p[1]) 
        waiting_nodes = self.get_nodes_at_depth(2)

        while (not waiting_nodes.is_empty()):
            rect = waiting_nodes.get_front().get_val() 
            waiting_nodes.dequeue()
            top_left = Vector.Point(rect.bottom_left[0], rect.top_right[1])
            bottom_right = Vector.Point(rect.top_right[0], rect.bottom_left[1])
            if (rect.depth < min(self.max_depth, depth)):
                if (f_point(top_left) > 0 and f_point(rect.top_right) > 0 and 
                    f_point(rect.bottom_left) > 0 and f_point(bottom_right) > 0):
                    self.shapeList.append(pyglet.shapes.BorderedRectangle(rect.bottom_left[0],
                                        rect.bottom_left[1],
                                        rect.width(),
                                        rect.height(),
                                        border_width,
                                        inside_color,
                                        border_color, 
                                        self.batch
                                        )
                    )
                    continue
                elif (f_point(top_left) < 0 and f_point(rect.top_right) < 0 and 
                    f_point(rect.bottom_left) < 0 and f_point(bottom_right) < 0):
                    self.shapeList.append(pyglet.shapes.BorderedRectangle(rect.bottom_left[0],
                                        rect.bottom_left[1],
                                        rect.width(),
                                        rect.height(),
                                        border_width,
                                        inside_color,
                                        border_color, 
                                        self.batch
                                        )
                    )
                    continue
                else:
                    for i in range(4):
                        if (rect.subrects[i] is not None):
                            waiting_nodes.queue(rect.subrects[i])
            else:
                self.shapeList.append(pyglet.shapes.BorderedRectangle(rect.bottom_left[0],
                                                        rect.bottom_left[1],
                                                        rect.width(),
                                                        rect.height(),
                                                        border_width,
                                                        inside_color,
                                                        border_color, 
                                                        self.batch
                                                        )
                                    )
