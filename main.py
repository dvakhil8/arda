# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd

def print_hi(name):
    df = pd.read_csv('/Users/zc-akhildv/Downloads/blocks.csv')
    print(df.head(100).to_string())
    print(df[df.gas_used>0].to_string())



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
