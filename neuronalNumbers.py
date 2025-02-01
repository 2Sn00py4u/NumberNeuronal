#imports
import ImageStyling as IM
import os

class number_neuronalNetwork():
    def __init__(self, Images:list) -> None:
        self.zeromap = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: []
        }
        self.train_data = {}
        for i in range(len(Images)):
            self.train_data[i] = IM.grayscale_Image_to_array(image_path=Images[i], shrink=False, scale=(0,1))

        
        for number in self.train_data:
            for i, line in enumerate(self.train_data[number]):
                for a, pixel in enumerate(line):
                    if pixel == 0.0:
                        self.zeromap[number].append((i, a))
                        
        #print(self.zeromap)
                            
        
        
    def train_model(self):
        pass

    def predict_model(self, Image_path_to_predict):
        # load zero_map of image to predict
        zeromap_predict_image = []
        Image_to_predict = IM.grayscale_Image_to_array(image_path=Image_path_to_predict, shrink=True, scale=(0,1))
        for i, line in enumerate(Image_to_predict):
            for a, pixel in enumerate(line):
                if pixel == 0.0:
                    zeromap_predict_image.append((i, a))
        count_zero = len(zeromap_predict_image)
        print(zeromap_predict_image, count_zero)
                    
        #compare to each number
        output = {}
        for number in self.zeromap:
            equal_pixel = 0
            for pixel in zeromap_predict_image:
                if pixel in self.zeromap[number]:
                    equal_pixel +=1
            output[number] = (equal_pixel/count_zero) *100
            
        return output
            
            
            

images=[]
img_list = os.listdir("NumberNeuronal\\traindata")
for i in range(len(img_list)):
    if img_list[i] != "train_numbers.csv":
        images.append(os.path.join("NumberNeuronal\\traindata", img_list[i]))

numberNeuro = number_neuronalNetwork(images)
output = numberNeuro.predict_model("NumberNeuronal\\test\\fünf.png")
for key in output:
    print(f"{key}: {output[key]}%")