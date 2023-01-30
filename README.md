# PFI GroupMe Calculator

The PFI (Present Funny Index), calculated as a function of a GroupMe user's statistics, is considered by leading researchers to be the only objective measure of what is referred to in scientific terms as "the funny". This project allows anyone to calculate PFI for their favorite group chats.

## How to Use

First, clone the repo and create a `.env` file in the root directory. We will use this file later. The FPI calculator is a collection of Python scripts. If you do not have Python installed, you can download the latest version from https://www.python.org/.

### Obtaining an Access Token

To use the tool, you will first need a GroupMe API access token. To obtain an access token, navigate to https://dev.groupme.com/ and create an account. Next, create an application. Your access token can then be found by clicking "Accesss Token" on the site's navigation bar.

Finally, open the `.env` file and paste in the following line but replace `[your_token_here]` with your access token.

```
ACCESS_TOKEN=[your_token_here]
```

### Finding the Group ID

To view the IDs of all groups you are in, you can run the `group-puller.py` script.

### Executing the Tool

The PFI calculator is a simple python script that first scrapes all messages from the desired GroupMe group and then performs a statistical analysis. There are three parameters to the pfi calculator script,

1. `group_id` - ID of the group to analyze.
2. `output_directory` - Path to the output `.csv` file
3. `[input_directory]` - Optional. Path to the input `.csv` file if messages have already been downloaded previously.

```
python pfi-calculator.py group_id output_directory [input_directory]
```
