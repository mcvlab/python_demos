# encoding: utf-8

from torch.utils.tensorboard import SummaryWriter


def main():
    writer = SummaryWriter("logs", filename_suffix=".capsule")
    writer.add_scalar("test", 0.1, 1)
    writer.close()


if __name__ == "__main__":
    main()
