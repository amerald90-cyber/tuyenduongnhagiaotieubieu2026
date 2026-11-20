import cv2
import numpy as np

# Load screenshot
img = cv2.imread(r'C:\Users\ADMIN\.gemini\antigravity\brain\b126fce1-b858-467d-a0a8-e5157db3878b\.user_uploaded\media_1795171653696_61a0c0ba.jpg')
h, w = img.shape[:2]

# In the screenshot, the query preview box is at the top left of the upload box
# Let's crop the query preview region
# In the screenshot: query-preview-img is around y: 90..170, x: 290..340
crop_query = img[90:175, 290:340]
cv2.imwrite('user_query_face.jpg', crop_query)
print('Cropped user query face box, saved to user_query_face.jpg')
