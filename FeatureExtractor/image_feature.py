import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import transforms
import pandas as pd

# implementation of Deiter's in Pytorch version https://www.kaggle.com/code/christofhenkel/extract-image-features-from-pretrained-nn/notebook
class FEDenseNetP(nn.Module):
    def __init__(self, num_channels=3):
        super().__init__()
        preloaded = torchvision.models.densenet121(weights=True)
        self.features = preloaded.features
        self.features.conv0 = nn.Conv2d(num_channels, 64, kernel_size=8, stride=2, padding=3)
        self.average_pool = nn.AvgPool1d(4)
        
        del preloaded
        
    def forward(self, x):
        
        # getting pretrained features
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

def get_image_features(img,id='pet_id'):
    
    m = FEDenseNetP()
    m.eval()
    # loadin from PIL requires transformations
    try : 
        img_t = transformer(img)
        img_t = torch.unsqueeze(img_t,0)
    except:
        img_t = img
        pass
    # fit the image to get the new weights
    y = m(img)
    # reduce dimension
    y = torch.squeeze(y)
    arr = y.data.numpy()
    features = {}
    features[id] = arr
    train_feats = pd.DataFrame()
    train_feats = pd.DataFrame.from_dict(features, orient='index')
    train_feats.columns = [f'pic_{i}' for i in range(train_feats.shape[1])]
    return train_feats
    
    
# get_image_features(torch.rand((1,3,256,256))) # ready to directly fit in the model when using torch tensor. comment all transformation before fitting.
