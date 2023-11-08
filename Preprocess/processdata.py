from FeatureExtractor import image_feature

def image_resize():
    pass

def get_image_features(img):
    img_feat = image_feature.get_image_features(img)
    return img_feat

def process(numerical, categorical, img, text):
    img_feat = get_image_features(img)
    #combine and return
    
    return img_feat