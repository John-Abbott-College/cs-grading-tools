import image_lists_final
from my_functions import throw_rocks, estimate_100_areas
test_image = image_lists_final.test_image
number_of_rocks = 50000 # you can change this if you want
max_size_of_image = 100 # this is kinda fixed
area = throw_rocks(number_of_rocks, max_size_of_image, test_image, True)
print(area)

student_id = 6302041
my_image = image_lists_final.images[student_id % 16]
area = throw_rocks(number_of_rocks, max_size_of_image, my_image, True)
print(area)

area = estimate_100_areas(500,max_size_of_image,test_image)
print(area)