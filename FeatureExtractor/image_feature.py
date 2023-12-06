import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import transforms
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from Configuration import config
import os
import concurrent.futures
from tqdm import tqdm
from PIL import Image

# implementation of Deiter's in Pytorch version https://www.kaggle.com/code/christofhenkel/extract-image-features-from-pretrained-nn/notebook
class FEDenseNetP(nn.Module):
    def __init__(self, num_channels=3):
        super().__init__()
        preloaded = torchvision.models.densenet121(pretrained=True)
        self.features = preloaded.features
        self.features.conv0 = nn.Conv2d(num_channels, 64, kernel_size=8, stride=2, padding=3)
        self.average_pool = nn.AvgPool1d(4)
        
        del preloaded

    def forward(self, x):
        features = self.features(x)
        out = F.adaptive_avg_pool2d(features, (1, 1)).view(features.size(0), -1)
        x = self.average_pool(out)
        return x

transformer = transforms.Compose([        # Defining a variable transforms
                    transforms.Resize(256),                # Resize the image to 256×256 pixels
                    transforms.CenterCrop(256),            # Centre Cropping the image to 256×256 pixels about the center
                    transforms.ToTensor(),                 # Convert the image to PyTorch Tensor data type
                    transforms.Normalize(                  # Normalize the image
                    mean=[0.485, 0.456, 0.406],            # Mean and std of image as also used when training the network
                    std=[0.229, 0.224, 0.225]      
                    )])






def get_image_features(img):
    
    m = FEDenseNetP()
    m.eval()
    # loadin from PIL requires transformations
    try : 
#         img_t = transformer(img)
        img_t = torch.unsqueeze(img_t,0)
    except:
        img_t = img
        pass
    # fit the image to get the new weights
    y = m(img)
    # reduce dimension
    y = torch.squeeze(y)
    arr = y.data.numpy()
    return arr


# function to process a single image and return its features
def process_image(image):
    features = {}
    input_tensor = transformer(image)
    input_batch = input_tensor.unsqueeze(0)
    
    feature = get_image_features(input_batch)
    
    
    train_feats = pd.DataFrame([feature], columns=[f'pic_{i}' for i in range(len(feature))])
    features = train_feats[[f'pic_{i}' for i in range(256)]].values
    # SVD reduction
    n_components = 32
    svd_ = TruncatedSVD(n_components=n_components, random_state=555)
    svd_col = svd_.fit_transform(features)
    svd_col = pd.DataFrame(svd_col)
    svd_col = svd_col.add_prefix('IMG_SVD_')
    return svd_col

   
def process_train(pet_id):
    
    filename_full = os.path.join(config.TRAIN_IMAGE_DIR, pet_id + '-1.jpg')
    if filename_full.endswith('-1.jpg'):
        image = Image.open(filename_full).convert('RGB')
        input_tensor = transformer(image)
        input_batch = input_tensor.unsqueeze(0)
        features = get_image_features(input_batch)
        return pet_id, features
    
    
def process_image_train():
    try:
        
        if os.path.exists(config.IMG_FEAT):
            print("Saved Densenet Feature found...loading features......\n")
            img_features = pd.read_csv("img_features_densenet121.csv", index_col=0)
            return img_features

        else :
            print("Preparing New using DenseNet Image Features............... ")
                # Get all filenames in the specified directory
            all_files = os.listdir(config.TRAIN_IMAGE_DIR)

            # Filter filenames to include only those ending with '-1.jpg'
            filtered_files = [filename[:-6] for filename in all_files if filename.endswith('-1.jpg')]

            # Get unique pet IDs
            unique_pet_ids = set(filtered_files)

            # Convert to a list
            unique_pet_ids_list = list(unique_pet_ids)
        
            # parallel processing
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Use tqdm to display progress
                with tqdm(total=len(unique_pet_ids_list), desc="Processing Images", unit="image") as progress_bar:
                    # Submit tasks to the executor and retrieve the results
                    futures = [executor.submit(process_train, pet_id) for pet_id in unique_pet_ids_list]
                    for future in concurrent.futures.as_completed(futures):
                        # Get the result and update the features dictionary
                        pet_id, img_feats = future.result()
                        features[pet_id] = img_feats
                        progress_bar.update(1)
                    
            train_feats = pd.DataFrame.from_dict(features, orient='index')
            train_feats.columns = [f'pic_{i}' for i in range(train_feats.shape[1])]
            train_feats = train_feats.reset_index()
            train_feats.rename({'index': 'PetID'}, axis='columns', inplace=True)
            
            # SVD reduction
            n_components = 32
            svd_ = TruncatedSVD(n_components=n_components, random_state=555)

            # features_df = pd.concat([train_feats, test_feats], axis=0)
            features = train_feats[[f'pic_{i}' for i in range(256)]].values

            svd_col = svd_.fit_transform(features)
            svd_col = pd.DataFrame(svd_col)
            svd_col = svd_col.add_prefix('IMG_SVD_')

            all_ids = pd.DataFrame({'PetID' : unique_pet_ids_list} )
            img_features = pd.concat([all_ids, svd_col], axis=1)
            img_features.to_csv(config.IMG_FEAT)
            
            return img_features

        
        
    except Exception as e:
        print("Error while reading the image directory", e)
        return pd.DataFrame()
    # get_image_features(torch.rand((1,3,256,256))) # ready to directly fit in the model when using torch tensor. comment all transformation before fitting.
