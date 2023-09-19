import numpy as np
import torch

from nvae.utils import add_sn
from nvae.vae_celeba import NVAE

if __name__ == '__main__':

    img_size = 64
    z_dim = 32
    cols, rows = 12, 12
    width = cols * img_size
    height = rows * img_size

    device = "cpu"
    model = NVAE(z_dim=32, img_dim=(128, 128))
    model.apply(add_sn)
    model.to(device)

    model.load_state_dict(torch.load("/logs/nvae/best_1.pth", map_location=device), strict=False)

    model.eval()

    result = np.zeros((width, height, 3), dtype=np.uint8)

    with torch.no_grad():
        z = torch.randn((cols * rows, z_dim, 1, 1)).to(device)
        gen_imgs, _ = model.decoder(z)
        print(gen_imgs.shape)
        gen_imgs = gen_imgs.reshape(rows, cols, 3, img_size, img_size)

        gen_imgs = gen_imgs.permute(0, 1, 3, 4, 2)
        gen_imgs = gen_imgs.cpu().numpy() * 255
        gen_imgs = gen_imgs.astype(np.uint8)

    for i in range(rows):
        for j in range(cols):
            result[i * img_size:(i + 1) * img_size, j * img_size:(j + 1) * img_size] = gen_imgs[i, j]

    from PIL import Image

    im = Image.fromarray(result)
    im.save("output/demo2.jpeg")
