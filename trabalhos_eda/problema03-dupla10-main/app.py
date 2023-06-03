import pyglet
from implicit import QuadTree
import Vector

class App: 
    TOTAL_MODES = 3
    """
    Application interface
    """
    def __init__(self, 
                window: pyglet.window.Window,
                tree: QuadTree, 
                avaliable_functions: Vector.StaticVector,
                root_color: tuple, positive_color: tuple, negative_color: tuple, 
                border_width: int = 1,
                inside_color: tuple = (0,0,0), border_color: tuple = (255,255,255)):
        self.updated_batch = False # starts false to avoid drawing before pressing C
        self.updated_tree = False
        self.window = window
        self.tree = tree
        self.program_depth = self.tree.max_depth # starts at the tree's depth, but can change independently of it
        
        self.mode = 1 # TODO review
        self.avaliable_functions = avaliable_functions # TODO review
        self.index = 0
        self.f = avaliable_functions[0]

        self.root_color = root_color
        self.positive_color = positive_color
        self.negative_color = negative_color
        self.inside_color = inside_color
        self.border_color = border_color
        self.border_width = border_width

    def update_info_label(self, color = (255, 255, 255, 255)):
        x0, y0 = self.window.get_size()[0]//25, self.window.get_size()[1]//10

        if (self.updated_batch and self.updated_tree):
            text = "Updated Information: depth={} | function={} | mode={}".format(self.program_depth,
                                                                                    self.index,
                                                                                    self.mode)
        else:
            text = "Outdated Information: depth={} | function={} | mode={}".format(self.program_depth,
                                                                                self.index,
                                                                                self.mode)
        self.label = pyglet.text.Label(text, font_name="Arial", 
                                        font_size=14, 
                                        x=x0,
                                        y=y0,
                                        color=color,
                                        anchor_x='left', anchor_y='bottom'    
                                        )
        # cover past labels with black background
        pyglet.shapes.Rectangle(x0, y0, self.label.content_width, 
                                self.label.content_height, color=(0,0,0)).draw()
        # draw current label over it
        self.label.draw()
    
    def generate_warning_if_outdated(self, color = (255, 255, 255, 255)):
        if (self.updated_tree is False): # consequently, self.updated_batch is also false
            text = "The tree does not correspond to current parameters. Press 'U' to update"
        elif (self.updated_batch is False): # but self.updated_tree is true
            text = "The batch does not correspond to current parameters. Press 'B' to update"
        else:
            return # nothing to warn
        
        x0, y0 = self.window.get_size()[0]//25, self.window.get_size()[1]//15
        self.warning = pyglet.text.Label(text, font_name="Arial",
                                            font_size=14,
                                            x=x0, 
                                            y=y0, 
                                            color=color,
                                            anchor_x="left", anchor_y="bottom")
        # cover past warnings with black rectangle
        pyglet.shapes.Rectangle(x0, y0, self.warning.content_width, 
                                self.warning.content_height, color=(0,0,0)).draw()
        # draw current warning
        self.warning.draw()
        
    def gameloop(self):
        """
        Default mode is assumed to be 1
        """
        self.make_batch = lambda : QuadTree.make_batch_curve(self.tree, 
                                                                self.f, 
                                                                self.root_color, 
                                                                self.program_depth)
        def on_draw():
            if (self.updated_batch and self.updated_tree):
                self.window.clear()
                self.tree.batch.draw()
                self.label.draw()

        def on_key_press(symbol: pyglet.window.key, modifiers):
            if (symbol == pyglet.window.key.C):
                # generate label and batch objects for the first time
                self.update_info_label()
                self.make_batch()
                self.updated_batch = True
                self.updated_tree = True
            
            elif (symbol == pyglet.window.key.B): # update only batch
                if (self.updated_batch is False):
                    self.make_batch()
                    self.updated_batch = True
                    self.update_info_label()
            
            elif (symbol == pyglet.window.key.U): # update both self.tree and batch
                if (self.updated_tree is False or self.updated_batch is False):
                    if (self.program_depth > self.tree.max_depth):
                        self.tree.max_depth = self.program_depth
                        self.tree.build_tree()
                    self.make_batch()
                    self.updated_batch = True
                    self.updated_tree = True
                    self.update_info_label()
            
            elif (symbol == pyglet.window.key.D):
                self.program_depth += 1
                if (self.program_depth > self.tree.max_depth):
                    # self.tree.max_depth = self.program_depth: only on update
                    self.updated_tree = False # self.updated_tree is false iff self.tree.max_depth changes
                self.updated_batch = False
                self.update_info_label()
                self.generate_warning_if_outdated()
            
            elif (symbol == pyglet.window.key.F):
                """
                Since it decreases depth, and the lower layers of the tree have already
                been built, it does not make self.updated_tree false.
                Minimum accepted depth is 2.
                """
                if (self.program_depth > 2):
                    self.program_depth -= 1
                    self.updated_batch = False
                    self.update_info_label()
                    self.generate_warning_if_outdated()

            elif (symbol == pyglet.window.key.M):
                self.mode = (self.mode) % App.TOTAL_MODES + 1 # cyclic shifting
                if (self.mode == 1):
                    self.make_batch = lambda : QuadTree.make_batch_curve(self.tree, 
                                                                            self.f,
                                                                            self.root_color, 
                                                                            self.program_depth)
                elif (self.mode == 2):
                    self.make_batch = lambda : QuadTree.make_batch_colored(self.tree, 
                                                                            self.f,
                                                                            self.positive_color,
                                                                            self.negative_color,
                                                                            self.root_color,
                                                                            self.program_depth)
                elif (self.mode == 3):
                    self.make_batch = lambda : QuadTree.make_batch_border(self.tree, 
                                                                            self.f,
                                                                            self.border_width,  
                                                                            self.border_color,
                                                                            self.inside_color,  
                                                                            self.program_depth)
                
                self.updated_batch = False
                self.update_info_label()
                self.generate_warning_if_outdated()

            elif (symbol == pyglet.window.key.N):
                self.index = (self.index + 1) % len(self.avaliable_functions)
                self.f = self.avaliable_functions[self.index]
                self.updated_batch = False
                self.update_info_label()
                self.generate_warning_if_outdated()
                
        self.window.on_draw = on_draw
        self.window.on_key_press = on_key_press
        pyglet.app.run()


