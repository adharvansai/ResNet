import numpy as np

""" This script implements the functions for data augmentation and preprocessing.
"""

def parse_record(record, training):
    """ Parse a record to an image and perform data preprocessing.

    Args:
        record: An array of shape [3072,]. One row of the x_* matrix.
        training: A boolean. Determine whether it is in training mode.

    Returns:
        image: An array of shape [3, 32, 32].
    """
    # Reshape from [depth * height * width] to [depth, height, width].
    depth_major = record.reshape((3, 32, 32))

    # Convert from [depth, height, width] to [height, width, depth]
    image = np.transpose(depth_major, [1, 2, 0])

    image = preprocess_image(image, training)

    # Convert from [height, width, depth] to [depth, height, width]
    image = np.transpose(image, [2, 0, 1])

    return image

def preprocess_image(image, training):
    """ Preprocess a single image of shape [height, width, depth].

    Args:
        image: An array of shape [32, 32, 3].
        training: A boolean. Determine whether it is in training mode.
    
    Returns:
        image: An array of shape [32, 32, 3].
    """
    if training:
        ### YOUR CODE HERE
        hpad = np.zeros((32,4,3))
        image = np.hstack((image,hpad))
        image = np.hstack((hpad,image))

        vpad = np.zeros((4,40, 3))
        image = np.vstack((image, vpad))
        image = np.vstack((vpad, image))

        #print(np.shape(image))
        # Resize the image to add four extra pixels on each side.

        ### YOUR CODE HERE

        ### YOUR CODE HERE
        # Randomly crop a [32, 32] section of the image.
        # HINT: randomly generate the upper left point of the image
        rx = np.random.randint(8)
        ry = np.random.randint(8)
        crp_img = image[rx:rx+32,ry:ry+32,:]
        #print(np.shape(crp_img))

        ### YOUR CODE HERE

        ### YOUR CODE HERE
        # Randomly flip the image horizontally.
        # for i in range(crp_img.shape[0]):
        #     crp_img[i] = np.fliplr(crp_img[i])
        rf = np.random.randint(2)
        if(rf == 0):
            crp_img = np.fliplr(crp_img)
        #print(np.shape(crp_img))
        image = crp_img


        ### YOUR CODE HERE

    ### YOUR CODE HERE
    # Subtract off the mean and divide by the standard deviation of the pixels.
    cmean = []
    cstd = []
    for i in range(np.shape(image)[2]):
        arr = image[:,:,i]
        cmean = np.mean(arr)
        cstd = (np.std(arr))
        lfn = lambda x : (x-cmean)/cstd
        image[:,:,i] = lfn(arr)
    #print(np.shape(image))

    ### YOUR CODE HERE

    return image