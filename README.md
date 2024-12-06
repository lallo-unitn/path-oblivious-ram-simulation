# Path ORAM Simulation

## Overview
This project simulates the Path ORAM protocol as part of an assignment for Secure Cloud Computing (Q1 2024). The goal is to hide the data access patterns from the cloud storage server, making two sequences of read/write operations indistinguishable. This implementation does not involve a real remote server or encryption of data blocks; rather, it focuses on evaluating the behavior of the stash under different configurations.

## Path ORAM Description
Path ORAM is a simple and efficient protocol proposed by Stefanov et al. for accessing data blocks in cloud environments in a way that conceals the data access pattern from the server. In this protocol, the data is stored in a binary tree structure, with each node containing a bucket of data blocks. The main components include:
- **Stash**: A temporary storage area to hold blocks retrieved by the client.
- **Position Map**: An array that associates each block with a leaf node.

The ORAM simulation in this project follows the standard Path ORAM access process:
1. **Remap Block**: A block is assigned a new random position.
2. **Read Path**: The path from a specific leaf to the root is read.
3. **Update Block**: Data is updated in case of a write operation.
4. **Write Path**: Blocks are written back to the tree, including any from the stash.

## Features
- Simulates Path ORAM operations including reading, writing, and remapping of blocks.
- Evaluates the stash behavior for different bucket sizes and path levels.
- Implements a sequential access pattern to collect stash size data.

### Stash Size Analysis
One key aspect of this project is analyzing the stash size behavior. Specifically, the simulation collects data on how often the stash reaches certain sizes and helps determine practical upper bounds for the stash size.

### Data Collection
The simulation runs for at least six million access operations, where blocks are read or written sequentially. The stash size is recorded after the initial three million accesses to analyze the steady-state behavior.

Two configurations are used for the simulation:
1. **N = 2ⁱ⁵, Z = 2** (bucket size of 2)
2. **N = 2ⁱ⁵, Z = 4** (bucket size of 4)

## Data Output
The collected data is written to a text file with the following format:
- The first line contains: `-1, s` (where `s` is the total number of accesses recorded).
- Subsequent lines contain: `i, si`, where `i` represents the stash size, and `si` represents the number of times the stash reached a size greater than `i`.

### Example Output:
```
-1, 3000000
0, 3000000
1, 1500000
2, 750000
```

## Graphical Representation
Using the collected stash size data, the project generates graphs that show:
- **X-axis**: Required stash size `R` (excluding `R = 0`).
- **Y-axis**: Probability `Pr[size(S) > R]` of the stash size being larger than `R`.

The graphs are generated for both bucket sizes (`Z = 2` and `Z = 4`) to provide insights into how the stash size varies with different bucket configurations.

## Prerequisites
- Python 3.x
- Matplotlib (for graph generation)

## How to Run
1. Clone the repository:
   ```
   git clone git@github.com:lallo-unitn/path-oblivious-ram-simulation.git
   ```
2. Run the ORAM simulation script:
   ```
   python oram/client/path_oram.py
   ```
3. The stash size data will be saved to `simulationX.txt` files, where `X` corresponds to different configurations.

## References
- Stefanov, E., et al. "Path ORAM: An Extremely Simple Oblivious RAM Protocol." In Proceedings of the 2013 ACM SIGSAC Conference on Computer & Communications Security (2013).

## License
This project is licensed under the MIT License.
