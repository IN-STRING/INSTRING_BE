from torch import nn

class CordModel(nn.Module):
  def __init__(self, n_class):
    super(CordModel, self).__init__()

    self.cnn = nn.Sequential(
        nn.Conv2d(in_channels=1, out_channels=64, kernel_size=3, stride=1, padding=1),
        nn.BatchNorm2d(64),
        nn.ReLU(inplace=True),

        nn.Conv2d(64,128,3,1,1),
        nn.BatchNorm2d(128),
        nn.ReLU(inplace=True),

        nn.Conv2d(128,256,3,1,1),
        nn.BatchNorm2d(256),
        nn.ReLU(inplace=True),
        nn.MaxPool2d(kernel_size=(12, 1))
    )

    self.lstm = nn.LSTM(256, 512, batch_first=True, bidirectional=True)


    self.fc = nn.Sequential(
        nn.Linear(1024, 512),
        nn.ReLU(),
        nn.Dropout(0.5),
        nn.Linear(512, n_class)
    )

  def forward(self, x):
    x = self.cnn(x)
    x = x.squeeze(2)
    x = x.permute(0,2,1)
    x, _ = self.lstm(x)
    x = self.fc(x)
    x = x.permute(0,2,1)
    return x