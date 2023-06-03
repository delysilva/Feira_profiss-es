# quick_sort em python
def partition(vector, left, right):
	pivot = vector[left]
	i = left
	for c in range(left + 1, right + 1):
		if vector[c] <= pivot:
			i += 1
			vector[i], vector[c] = vector[c], vector[i]

	vector[left], vector[i] = vector[i], vector[left]
	return i


def quick_sort(vector, left, right):
	if left < right:
		pivot_index = partition(vector, left, right)
		quick_sort(vector, left, pivot_index - 1)
		quick_sort(vector, pivot_index + 1, right)

	return vector


### teste

lista = [10, 8, 100, 5, 1, 0, 6, 99, 55, 75]

print(quick_sort(lista, 0, len(lista) - 1))
