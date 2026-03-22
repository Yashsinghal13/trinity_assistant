# How to create a Journey Or Steps to create the Journey ?
## 1. Step 1 : Go to the Trinity UI and Search for the Go Planner.
## 2. Step 2 : Click on Add Journey at the Top Left
## 3. Step 3 : Give the Configuration Detail for Creating the Journey like :
### 3.1. Journey Name : Uniquely Identify Name.
### 3.2. Select the Intial Audience(It is for the Entry Node)
### 3.3. Select the Check box whether the User is allowed for the Re-Entry in Journey or not it is for the Reccurrence of Journey 
### 3.4. Select the Control Percentage which is used for control treament in the Engamement Node
### 3.5. Now Select the Campaign Crc it is used for the breaking down the audience into control and treatment if not selected then by default journeny name is selected as hash.
### 3.6. Now select the kpi based response
### 3.7 Select start Date on which journey should be started
## 4. Step 4 : Now the entry Nodes get added in the UI and you will see different types of Segement Node ,Engagement Node and Controller Node.
## 5. Step 5 : Now add any of the Node according to the requirement and fill the Configuration of node added
## 6. For the Connection Please Let me know about the rules


# Rules of Segment Node:
A Segment Node in a Journey can connect to multiple types of nodes, enabling flexible flow control and audience branching. Specifically, a Segment Node can lead to:

## Input Connection
1. Segment Node
2. Entry Node
3. Engagement node 
4. Engagement Split


## Output Connection
1. Another Segment Node
2. Force Exit Node 
3. Delay Time Node

# Rules of Entry Node :
An Entry Node in a Journey can connect to multiple types of nodes, enabling flexible flow control and audience branching.

## Input Connection
- NO input Connection

# Output Connection
1. Another Segment Node
2. Force Exit Node 
3. Delay Time Node

# Rules of Engagement Node :
An Engagement Node can connect to the following nodes in a Journey:

## Input Connection 
1. Delay Node

## Output Connection  
1. Segment Node
2. Force Exit (Controller Node)
3. Delay Time Node (Controller Node)
4. Engagement Split Node (Controller Node)
