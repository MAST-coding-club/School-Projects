import pygame
from math import sqrt, radians, tan
from numpy import dot

# Initialize Pygame
pygame.init()

#Condigure Values
screen_width = 600
screen_height = 400

num_of_div_x = 600
num_of_div_y = 400

px = 0
py = 0 

#Classes 
class Sphere:
    def __init__(self, center, radius,color):
        self.center = center
        self.radius = radius
        self.color = color 


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def intersection(self,sphere):
        oc = [sphere.center[i] - self.origin[i] for i in range (3)]
        a = dot(self.direction, self.direction)
        b =  -2 * dot(self.direction, oc)
        c = dot(oc,oc) - sphere.radius*sphere.radius

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return -1, None
        
        sqrt_d = sqrt(discriminant)
        t = (-b - sqrt_d) / (2 * a)
        intersection_vector = [self.origin[i] + t * self.direction[i] for i in range(3)]
        return t, intersection_vector
        
    def normal(self, sphere, point):
        normal = [point[i] - sphere.center[i] for i in range(3)]
        length = sqrt(sum(normal[i]**2 for i in range(3)))
        normalized_vector = [normal[i] / length for i in range(3)]
        return normalized_vector

def normalize(point):
    length = sqrt(sum(point[i]**2 for i in range(3)))   
    return  [point[i] / length for i in range(3)]
class SceneLight:
    def __init__(self, position, light_color, light_intensity):
        self.position = position
        self.light_color = light_color 
        self.light_intensity = light_intensity
        



#Objects and Scene
light = SceneLight([-1,-10,-10],(255,255,255), (1,1,1))
intensity_ambient = 0.2
intensity_specular = 10
sphere1 = Sphere([0, 0, 100], 20, (0,0,255))
sphere2 = Sphere([60,0,100],20, (0,255,0))
sphere3 = Sphere([-60,0,100],20, (255,0,0))


diffuse = 0.8
camera_origin = [0,0,0]
cam_look_vector = [0,0,1]
FOV = 90
focal_length = screen_width / (2*tan(radians(FOV)/2))    
# Set the title of the window
pygame.display.set_caption("Raytracer")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))

#Screen Calculation
pix_x_increment = screen_width / num_of_div_x
pix_y_increment = screen_height / num_of_div_y

# Calculate positions
x_all_pos = []
y_all_pos = []

for px in range(0, int(screen_width), int(pix_x_increment)):
    if px not in x_all_pos:
        x_all_pos.append(px)
for py in range(0, int(screen_height), int(pix_y_increment)):
    if py not in y_all_pos:
        y_all_pos.append(py)


# Calculate the increments for each step to get the gradient 

red_color_inc = 135 / len(y_all_pos) if len(y_all_pos) > 1 else 0
green_color_inc = 75/len(y_all_pos) if len(y_all_pos) > 1  else 0
for y_index, y in enumerate(y_all_pos):
    gradient_color = (120 +red_color_inc*y_index, 180 + green_color_inc*y_index, 255)
    for x in x_all_pos:
        def renderer(sphere):
            ray_direction = [
                (x - screen_width / 2) / focal_length,
                (y - screen_height / 2) / focal_length,
                1
            ]
            ray_direction = normalize(ray_direction)

            ray = Ray(camera_origin, ray_direction)
            t, intersection_vector = ray.intersection(sphere)

            if t > 0:
                light_length = sqrt(sum((light.position[i]-intersection_vector[i])**2 for i in range(3)))
                light_direction = [light.position[i] - intersection_vector[i] for i in range(3)]
                normalized_light = [light_direction[i] / light_length for i in range(3)]
            
                surface_normal = ray.normal(sphere, intersection_vector)
                vector_to_camera = [camera_origin[i] - intersection_vector[i] for i in range(3)]
                half_vector = [light_direction[i] + vector_to_camera[i] for i in range(3)]
                half_vector = normalize(half_vector)
            

                specular_strength = max(0, dot(surface_normal, half_vector)) ** intensity_specular
                dp = dot(normalized_light, surface_normal)
                specular_color = [specular_strength * light.light_color[i] for i in range(3)]
                diffuse_color = max(0, dp) * diffuse 
            
                #Color calculation
                final_color = [
                            min(255, int(intensity_ambient * sphere.color[i] +
                            diffuse_color * sphere.color[i] +
                            specular_color[i]))
                            for i in range(3)
                              ] 
                screen.set_at((x,y), final_color)
            
        renderer(sphere1)
        renderer(sphere2)
        renderer(sphere3)
       
            

pygame.display.flip()
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False
        
    clock.tick(60)

# Quit Pygame
pygame.quit()