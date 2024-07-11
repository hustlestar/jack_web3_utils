
# Ethereum Fancy Address Generator

This script generates an Ethereum new address with specified start and/or end. It also supports generating the address using a seed phrase.

## Prerequisites

Make sure you have Python installed on your system. You will also need to install the required libraries:

```sh
pip install eth-account eth-utils
```

# Usage

## Command Line Arguments Arguments for Ethereum Address Generator

The Ethereum address generator allows you to create one or more Ethereum addresses with specified criteria, including optional seed phrases for added security. Below are the available command-line arguments for this tool:

### `--address-start`

- **Description**: Specifies the desired starting substring(s) of the Ethereum addresses to be generated. You can specify multiple starting substrings separated by spaces.
- **Usage**:
  ```bash
  --address-start prefix1 prefix2
  ```
- **Default**: If not specified, the address can start with any substring.
- **Example**:
  ```bash
  --address-start 00 69
  ```

### `--address-end`

- **Description**: Specifies the desired ending substring(s) of the Ethereum addresses to be generated. You can specify multiple ending substrings separated by spaces.
- **Usage**:
  ```bash
  --address-end suffix1 suffix2 ...
  ```
- **Default**: If not specified, the address can end with any substring.
- **Example**:
  ```bash
  --address-end 000 69
  ```

### `--number-of-addresses`

- **Description**: Sets the number of Ethereum addresses to generate.
- **Usage**:
  ```bash
  --number-of-addresses number
  ```
- **Default**: `1`
- **Example**:
  ```bash
  --number-of-addresses 3
  ```

### `--use-seed-phrase`

- **Description**: Enables the generation of a seed phrase for each Ethereum address. This option increases the security of the generated addresses but may slow down the generation process significantly.
- **Usage**:
  ```bash
  --use-seed-phrase
  ```
- **Default**: Disabled unless specified.
- **Example**:
  ```bash
  --use-seed-phrase
  ```

### `--number-of-seed-phrase-words`

- **Description**: Determines the number of words in the seed phrase, if seed phrase generation is enabled.
- **Usage**:
  ```bash
  --number-of-seed-phrase-words 24
  ```
- **Default**: `12`
- **Example**:
  ```bash
  --number-of-seed-phrase-words 12
  ```
---

```sh
python web3_address_generator.py --address-start 123 --address-end abc --use-seed-phrase
```

This command will generate an Ethereum address that starts with `123` and ends with `abc`, using a seed phrase for the address generation.

## Script Explanation

Here is a concise Markdown document that explains the functionality of your Python script for generating Ethereum addresses based on user-defined criteria:

---

## Ethereum Address Generator Script Documentation

This script automates the generation of Ethereum addresses with optional start and end substrings, and optionally includes a seed phrase for enhanced security.

### Functions

- **`preprocess_address_starts(starts)`**: Processes the starting substrings by removing '0x' and converting to lowercase.
- **`generate_new_eth_address_with_seed_phrase(starts, ends, number_of_seed_phrase_words)`**: Generates a new Ethereum address with a seed phrase, matching the specified start and end substrings.
- **`generate_new_eth_address_without_seed_phrase(starts, ends)`**: Generates a new Ethereum address without a seed phrase, matching the specified start and end substrings.
- **`address_matches(address, start, end)`**: Checks if a given address matches the specified start and end substrings.
- **`print_generation_result(address, key, seed_phrase)`**: Prints the Ethereum address, private key, and seed phrase (if applicable).
- **`start_generation_job(starts, ends, number_of_addresses, use_seed_phrase, number_of_seed_phrase_words)`**: Manages the generation of multiple Ethereum addresses.
- **`prepare_generation_job(ends, number_of_addresses, number_of_seed_phrase_words, starts, use_seed_phrase)`**: Prepares and validates the parameters for the generation job.
- **`generate_address(number_of_addresses, starts, ends, use_seed_phrase, number_of_seed_phrase_words)`**: Coordinates the preparation and execution of the address generation.

### Example Command
From the same directory where `web3_address_generator.py` is located run: 

```bash
python web3_address_generator.py --address-start 1a3 1b4 --address-end abc def --number-of-addresses 5 --use-seed-phrase --number-of-seed-phrase-words 24
```

This command will generate 5 Ethereum addresses that start with '1a3' or '1b4', end with 'abc' or 'def', each with a 24-word seed phrase.

---

## Google Collab

If you trust Google enough - you may run this script in the Google collab, but I would not advise to do so. 

[Google Collab Notebook](https://colab.research.google.com/drive/1TAZZvmnSMD67SfLfRiCChCBJgVnMMX7c?usp=sharing)

---
## Code

Here is the full script [web3_address_generator.py](web3_address_generator.py)


## Notes

- Generating new address can take a significant amount of time, especially if the start or end is long.
- Be careful with the generated private key and seed phrase. Store them securely.
