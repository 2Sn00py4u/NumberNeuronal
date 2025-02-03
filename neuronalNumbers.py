#imports
import ImageStyling as IS
import os, numpy

def imageCSV_to_traindata(csv_file):
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
        9: [],
        "paths": []
    }
    if type(csv_file) == str:
        with open(csv_file, "r") as images_csv:
            for i,line in enumerate(images_csv):
                if i != 0:
                    paths = line.split(";")
                    paths.pop(len(paths)-1)
                    for n in range(10):
                        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),paths[n])
                        train_data["paths"].append(paths[n])
                        train_data[n].append(IS.grayscale_Image_to_array(image_path, scale=(0,1)))
            images_csv.close()
        return train_data

class number_neuronalNetwork():
    def __init__(self, Images:str) -> None:
        self.data_file = Images
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
        
        self.train_data = imageCSV_to_traindata(Images)
        def get_self_zeromap():
            for number in self.train_data:
                if number != "paths":
                    for i in range(len(self.train_data[number])):
                        number_zeromap = []
                        for line_index,line in enumerate(self.train_data[number][i]):
                            for pixel_index in range(len(line)):
                                if line[pixel_index] == 0.0:
                                    number_zeromap.append((line_index,pixel_index))
                        self.zeromap[number].append(number_zeromap)
        get_self_zeromap()
        
          
    def train_model(self, train_data_csv):
        train_data = imageCSV_to_traindata(train_data_csv)
        paths_to_append = ""
        for number in train_data:
            for image in train_data[number]:
                prediction = self.predict_model(image)
                prediction_values = []
                for prediction_number in prediction:
                    if type(prediction_number) == int:
                        prediction_values.append((prediction[prediction_number],prediction_number))
                prediction_values.sort(reverse=True)
                #print(prediction_values)
                if number != "paths":
                    if prediction_values[0][1] == number:
                        print(f"success with image: {train_data["paths"][number]}| result: {number} == {prediction_values[0][1]} ({prediction[number]})")
                    else:
                        print(f"FAILED with image: {train_data["paths"][number]}| result: {number} ({prediction[number]}) != {prediction_values[0][1]} ({prediction_values[0][0]})")
            if type(number) == int:            
                paths_to_append += train_data["paths"][number] + ";"
        print(paths_to_append)
            
        with open(self.data_file, "a") as append_file:
            append_file.writelines(f"{paths_to_append}\n")
            append_file.close()   

                    

    def predict_model(self, image_to_predict:str|numpy.ndarray):
        #  load zero_map of image to predict
        zeromap_predict_image = []
        if type(image_to_predict) == str:
            Image_to_predict = IS.grayscale_Image_to_array(image_path=image_to_predict, shrink=True, scale=(0,1))
        else:
            Image_to_predict = image_to_predict
        
        #  get zeromap    
        for i, line in enumerate(Image_to_predict):
            for a, pixel in enumerate(line):
                if pixel == 0.0:
                    zeromap_predict_image.append((i, a))
        count_zero = len(zeromap_predict_image)
        #print(zeromap_predict_image, count_zero)
                    
        #  comparing zeromap
        output = {}
        for number in self.zeromap:
            #print(number)
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
                #print(Zwischenergebnis)
                output[number] += Zwischenergebnis
            output[number] = output[number]/len(self.zeromap[number])   
        return output
            
            
            

images=[]
img_list = os.listdir("traindata")
for i in range(len(img_list)):
    if img_list[i] != "train_numbers.csv":
        images.append(os.path.join("traindata", img_list[i]))

numberNeuro = number_neuronalNetwork("traindata\\train_numbers.csv")

numberNeuro.train_model(train_data_csv="testdata\\test_data.csv")

"""
output = numberNeuro.predict_model("traindata\\9\\ninetest.jpg")
for key in output:
    if type(key) == int:
        print(f"{key}: {output[key]}%")
    elif type(key) == str:
        print(f"{key}: {output[key]} time(s)")"""
