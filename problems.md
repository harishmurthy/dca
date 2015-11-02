1. Create a URL shortener library (e.g., bitly). Given a long URL, your program should return a 
shortened URL. Ensure the following: 
a. for a long URL X, your program should always return the shortened URL x 
b. the short URLs your program returns, must not follow any pattern; successive calls to 
your program should return very different short URLs (e.g., GOOD: a1x2l3, zAb3gr, ... BAD: 
a1x213, a1x214, ...)  
c. for two different long URLs X and Y, your program should (ideally) always return two 
different shortened URLs x and y 
d. your program must be able to accept long URLs provided both through console as well 
as from a file of newline separated long URLs 
e. the program should work for input files with up to 100000 URLs without crashing 
f. we should be able to import your code as a module and use it (e.g., import shortener; 
short_url = shortener.shorten(long_url)) 
 
2. A Merkle Tree is a specialized hash structure often used to verify if the contents of two or 
more large files are the same in an efficient way. Please refer to Wikipedia and other sources on 
the web to understand how Merkle Trees work. Your task is to implement a Merkle Tree library in 
Python. Given paths to two files, your program should tell us whether the two files have the same 
content or not. Additionally, it'll be great if your program also tells us where (say, which file block) 
the differences are and prints the differences. Expect text files with sizes up to 5MB as inputs. 
 
3. Write a specialized sorting program that has the following functionality: 
a. External Sorting: External Sorting techniques are used when the amount of data to be 
sorted does not fit in main memory. Input will be a directory containing one or more large text 
files. Each file will have a newline separated element. Your output should be a single file with all 
elements sorted. 
b. Rotation of a Sorted List: Write a method 'rotate' that: (1) takes as input, N, the number 
of elements, and r, the number of times the list has to be rotated, (2) rotates the list 'r' times and 
writes the rotated list to a file. (rotation e.g., [1, 2, 3, 4, 5, 6] after 2 rotations [5, 6, 1, 2, 3, 4]) 
c. Random Number of Rotations: The above method should also allow for a random 
number of rotations in case 'r' is not specified. If 'r' is not specified, r = random.choice(range(0, 
N))  
d. Minimum Element in a Rotated Sorted List: Assume a sorted list of numbers of length 
N. Suppose that list has been rotated by a random 'r'. Write a method that returns the minimum 
element of a sorted rotated list. 
Expect total amount of data to be up to 2 GB (might be distributed across smaller files). At least 
parts a, b, and c of your program should work with data of this size without crashing. 
 
4. Write a simulator for a HeartBeat Monitoring System to monitor the health of a large number of 
machines based on the following description. (We have proposed a way of simulating this at the 
end of this problem. You can use reasonable alternatives.) a. when the program starts, it takes as input 'N' (the number of machines), 'f' (percentage 
of machines that will fail every 5 seconds), and 't' (number of seconds taken by a failed machine 
to recover) 
b. the program provides a shell where we can enter certain commands (listed below); the 
program only terminates when we enter the command 'quit' 
c. your program should support the following commands: (1) add_machines m_1, m2, 
..., (2) remove_machines m_1, m2, ..., (3) is_machine_alive m_1, prints 'True', 'False', or 
'machine not present', (4) num_machines_alive, prints the number of machines that are alive, 
(5) failure_trend, prints a list where each element is the number of machines that were alive 
based on a probe done every second (e.g., 27 27 25 22 27 32 shows there were 27 machines 
alive at the 1st second, 25 at the 3rd second, etc.) 
Simulation Set up: 
(1) Create a directory to represent a machine 
(2) Create a file named 'alive' inside a directory to indicate that the machine is alive 
(3) Use a timer that goes off every 5 seconds. A thread (or a process) gets triggered once the 
timer goes off, chooses N * f directories (machines) randomly and delete the 'alive' file from 
them to indicate that those machines are not alive 
(4) Use another timer that goes off every second and triggers a probe that checks how many 
machines are alive 
(5) Similarly, initiate a recovery process after every 't' seconds. The recovery process should 
recreate the 'alive' file in all the failed machines. 
 
5. Write a simulator for a Distributed Deployment system that deploys a set of files (code, config, 
etc.) on a large number of machines. You are expected to use some of the functionality you built 
in Problem 2 (Merkle Tree) and Problem 4 (Heartbeat Monitor). Write the simulator based on the 
following description. 
a. your program takes as input, path to a directory that has the files you need to deploy 
b. when you do a deployment, you do it on all machines that are alive when you start the 
deployment process (use Problem 4 to find out all machines that are alive); deployment means 
copying the contents of the input directory to the target directory representing a machine 
c. every 't' seconds ('t' is given in Problem 4), you run a probe to find out the machines 
that have recovered from failure; you do a deployment on the machines that have now become 
alive 
d. you continue probe­deployment cycles until: (1) you have deployed the files on every 
machine in the system, and (2) every machine has the same file contents (use Problem 2 to 
verify this). 
e. your program terminates with the message 'deployment successful on N machines' 
once the above conditions are satisfied. 
 
 
 