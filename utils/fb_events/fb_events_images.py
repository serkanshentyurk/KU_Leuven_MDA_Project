from PIL import Image
from utils import paths

res_pred_dist = Image.open(paths.path_fb_res_pred_dist_50)
feature_importance = Image.open(paths.path_fb_feature_importance_50)
other_plot = Image.open(paths.path_fb_other_plot_50)


