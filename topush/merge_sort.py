#merge sort em python

def merge(v, left, mid, right):
    help = (right+1)*[0]
    for i in range(0, right + 1):
        help[i] = v[i]

    i = left
    j = mid + 1
    k = left

    while i <= mid and j <= right:

        if help[i] <= help[j]:
            v[k] = help[i]
            i += 1
        else:
            v[k] = help[j]
            j += 1
        k+=1

    while i <= mid:
        v[k] = help[i]
        i += 1
        k += 1
    while j <= right:
        v[k] = help[j]
        j += 1
        k += 1


def merge_sort(values, left, right):
    if left >= right:
        return values
    else:
        mid = (left + right)//2
        merge_sort(values, left, mid)
        merge_sort(values, mid + 1, right)

        merge(values, left, mid, right)

    return values

v = [1, 5, 10, 3, 77, 18, 9, 0, 71]

print(merge_sort(v, 0, len(v) - 1))
  
