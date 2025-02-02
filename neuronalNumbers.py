#imports
import ImageStyling as IS
import os

class number_neuronalNetwork():
    def __init__(self, Images:list|str) -> None:
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
        def get_traindata():
            train_data = {
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
            if type(Images) == list:
                for i in range(len(Images)):
                    train_data[i] = IS.grayscale_Image_to_array(image_path=Images[i], scale=(0,1))
                return train_data
            elif type(Images) == str:
                with open(Images, "r") as images_csv:
                    for i,line in enumerate(images_csv):
                        if i != 0:
                            paths = line.split(";")
                            paths.pop(len(paths)-1)
                            print(paths)
                            for n in range(len(paths)):
                                print(f"including: {os.path.join(os.path.dirname(os.path.abspath(__file__)),paths[n])}")
                                train_data[n].append(IS.grayscale_Image_to_array(image_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), paths[n]), scale=(0,1)))
                    images_csv.close()
                return train_data    
        self.train_data = get_traindata()
        
        for number in self.train_data:
            for i in range(len(self.train_data[number])):
                number_zeromap = []
                for line_index,line in enumerate(self.train_data[number][i]):
                    for pixel_index in range(len(line)):
                        if line[pixel_index] == 0.0:
                            number_zeromap.append((line_index,pixel_index))
                self.zeromap[number].append(number_zeromap)
        print(self.zeromap[1])
        
    def train_model(self, train_data_csv):
        pass

    def predict_model(self, Image_path_to_predict):
        # load zero_map of image to predict
        zeromap_predict_image = []
        Image_to_predict = IS.grayscale_Image_to_array(image_path=Image_path_to_predict, shrink=True, scale=(0,1))
        for i, line in enumerate(Image_to_predict):
            for a, pixel in enumerate(line):
                if pixel == 0.0:
                    zeromap_predict_image.append((i, a))
        count_zero = len(zeromap_predict_image)
        print(zeromap_predict_image, count_zero)
                    
        #compare to each number
        output = {}
        for number in self.zeromap:
            print(number)
            output[number] = 0
            output[f"complete match ({number})"] = 0
            for i in range(len(self.zeromap[number])):
                equal_pixel = 0
                for pixel in zeromap_predict_image:
                    if pixel in self.zeromap[number][i]:
                        equal_pixel +=1
                Zwischenergebnis = (equal_pixel/count_zero) *100
                if Zwischenergebnis == 100:
                    output[f"complete match ({number})"] +=1
                print(Zwischenergebnis)
                output[number] += Zwischenergebnis
            output[number] = output[number]/len(self.zeromap[number])
            
        return output
            
            
            

images=[]
img_list = os.listdir("traindata")
for i in range(len(img_list)):
    if img_list[i] != "train_numbers.csv":
        images.append(os.path.join("traindata", img_list[i]))

numberNeuro = number_neuronalNetwork("traindata\\train_numbers.csv")

output = numberNeuro.predict_model("traindata\\1\\number1.png")
for key in output:
    if type(key) == int:
        print(f"{key}: {output[key]}%")
    elif type(key) == str:
        print(f"{key}: {output[key]} time(s)")