# Components of Journey Builder and User Journey or Go Planner

**Note** : Execution Date is the date at which the date the audience is evaluate and Send date is the date at which the audience is evaluate.

## Journey Nodes:
Nodes represent different stages or actions in the user journey. There are four main types:

1. Entry Node
2. Segment Node
3. Engagement Node
4. Controller Node

### 1. Entry Node
The Entry Node is the starting point of the Journey and is defined during its creation.
It specifies the base audience that enters the Journey based on user attributes such as days_since_registration, days_since_last_activity, purchase_amount_lifetime, and others.

Types of Users in Entry Node:
The Entry Node in a Journey defines who enters the Journey. Users can be included based on two types of criteria:

Attribute-Based Entry (Existing Attributes)
Users are selected based on pre-calculated user attributes at the time the Journey begins.

Example:
- Users with days_since_last_activity > 14
- Users with purchase_amount_lifetime > 1000
- Users with platform = Android

**Important Notes**

- If an audience is created using an Existing Target Group, it will not be available for selection in the audience dropdown anywhere within the Journey.
- No new users will be added after the Journey starts.
- Filters or conditions in later steps apply only to this initial user group.

**Entry Node Connections**:
An Entry Node in a Journey can connect to multiple types of nodes, enabling flexible flow control and audience branching.
- Another Segment Node
- Force Exit Node 
- Delay Time Node


### 2.Segment Node :
Segment Nodes act as smart filters within a Journey. They apply conditional checks on users flowing in from the previous node, based on user attributes.

### How Segment Nodes Work
Each Segment Node evaluates users against a specific condition (e.g., made a purchase in the last 1 day, opened the app recently, etc.).
Based on whether the user meets or does not meet the condition, they are routed down:
A Yes path (if the condition is met), or
A No path (if the condition is not met).

**Example Scenario:**

1. Assuming a user has already passed an earlier filter: Lifetime Purchase Value > ₹1000
2. Now, a Segment Node checks: Purchase Amount Last Day > 0
3. If the user meets this new condition, they follow the Yes path. The logic applied becomes:
- **Lifetime Purchase Value > ₹1000 AND Purchase Amount Last Day > 0**
- **If the user does not meet the condition, they follow the No path, and the logic becomes:**
Lifetime Purchase Value > ₹1000 AND NOT Purchase Amount Last Day > 0
 
### Key Benefits:
- Enables dynamic filtering within a Journey.
- Builds progressive logic as users move through steps.
- Ensures personalized targeting by evaluating user behavior.

**Important Notes**
If an audience is created using an Existing Target Group, it will not be available for selection in the audience dropdown anywhere within the Journey.

### Segment Node Connections:
A Segment Node in a Journey can connect to multiple types of nodes, enabling flexible flow control and audience branching. Specifically, a Segment Node can lead to:
1. Another Segment Node
2. Force Exit Node 
3. Delay Time Node


### 3.Engagement Nodes:
Engagement Nodes are interaction points in a Journey where users are engaged through targeted communication. These nodes define which channel to use, what message to send, and how long to wait for user interaction.

Engagement Node Components

1. Channel

The medium through which messages are sent to users like (Email, SMS, Push Notification, In-app Messages, and more).

2. Template

- A Template is a predefined message format used to communicate with users across various channels such as Push Notifications, Email, SMS, In-App Messages, and more.
- Templates define the structure and content of a message, including:
- Text or visual content (depending on channel)
- Links or call-to-action buttons
- Personalization fields (e.g., user name, location, last activity)

3. Qualifying Window

- A waiting period after sending the message during which the system tracks user engagement.
- Common engagement metrics include sent, open, click, delivered.
- After the window expires, the Journey continues based on whether or not the user interacted.
- The waiting period begins from the day the campaign is actually sent to the user — not from the campaign execution date.

**For example**, if the campaign data was executed on 20th July, but the campaign was sent on 22nd July, and the waiting period is 2 days, then:

The wait starts on 22nd July.

The next step in the Journey will execute on 24th July.

**Note:** Engagement Nodes can only be connected via Delay Time Nodes.

**Engagement Node Connectivity**
An Engagement Node can connect to the following nodes in a Journey:

1. Segment Node
2. Force Exit (Controller Node)
3. Delay Time Node (Controller Node)
4. Engagement Split Node (Controller Node)


### 4.Controller Node:
Controller Nodes allow you to control the flow of a Journey by introducing logic such as delays, force exits, or branching based on engagement behavior.

**Types of Controller Nodes:**
- Force Exit
- Delay Time Node
- Engagement Split

**1. Force Exit :**
    Used to remove a user from the Journey when they: 
    No longer meet certain conditions, or Fail to engage with previous steps (e.g., didn't open or click a message)
    Helps keep the Journey clean, efficient, and relevant.
    Prevents users from continuing through steps that are no longer applicable to them.

**2. Delay Time Node :**
    A Delay Time Node pauses the user journey for a set time, delaying when the next engagement is sent.
    This pause is based on the campaign sent time, not the node execution date.

    If Delay Time = 2 days:
    The Journey starts on 20th July.
    The campaign is sent on 22nd July.
    The user data for the campaign is evaluated on 20th July.

**3. Engagement Split**
    Splits the Journey path based on how users responded to a previous engagement (e.g., email, push notification).
    Enables behavior-based branching to personalize the user experience.

    Users can be segmented based on their interaction with the message — such as open, clicked, or delivered etc.

### Controller Node Connectivity

#### Delay Time Node can connect to:
- Engagement Node

#### Engagement Split Node can connect to:
- Segment Node
- Force Exit Controller Node
- Delay Time Node
- Another Engagement Split Node













