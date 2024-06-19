"""
Code Snippet from Kiran - study and re-write.
"""

def heap_add_or_replace(heap=[], heap_operation=None, heap_triplet=(None,None,None)):

    # Check data


    # Check 1: empty heap, append to stack

    print(heap)

    if len(heap)==0 :

        print('empty heap')

        heap.append(heap_triplet)

        return heap
   

    # Check 2: triplet exists in heap

    if (heap_operation == 'add'):

        print('add')

        heap_key = heap_triplet[0] 

        heap_value = heap_triplet[1] 

        heap_parent = heap_triplet[2] 

        

        # traverse through heap and check if the triplet exists

        for i, h in enumerate(heap) :

            if ( (h[0]==heap_key) and (h[1]>heap_value)) :

                heap[i] = heap_triplet

                return heap

        return heap

   

    # Check 3: triplet to be removed

    elif (heap_operation == 'remove'):

        print('remove')

        heap_sort_on_dist = sorted(heap, key= lambda x: x[1])

        min_heap = heap_sort_on_dist.pop(0)

   

        return min_heap

   

    # if all else fails

    return None

       

# main calling function

# triplet: (vertex, distance, parent)

triplet1 = ((2,3),0.9, (1,0))

triplet2 = ((1, 2), 0.01, (2, 0))

 

# check implementation: empty stack

heap1 = []

heap1 = heap_add_or_replace(heap=heap1, heap_triplet=triplet1)

print(heap1)

 

# check implementation: replace if lower

heap2 = [((2,3),0.99, (1,0)), ((1, 2), 0.001, (2, 0))]

heap2 = heap_add_or_replace(heap=heap2, heap_operation='add', heap_triplet=triplet2)

print(heap2)

   

# remove element

heap2 = [((2,3),0.99, (1,0)), ((1, 2), 0.001, (2, 0)),

         ((4,4), 0.00001, (0,0))]

heap2 = heap_add_or_replace(heap=heap2, heap_operation='remove' )

print(heap2)

#%%

