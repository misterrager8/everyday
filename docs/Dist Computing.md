# A Thorough Introduction to Distributed Systems

- Distributed system - a system with multiple servers so data and requests for data don’t rely on just one node.
    - Horizontal scaling - adding more servers of the same specs for better performance
    - Vertical scaling - upgrading a single server to have much better and faster equipment
- Fault tolerance - if there's a crash in one server, can the other server(s) pick up where they left off?
- Latency - speed at which data is sent or requested. The lower the latency, the better
- CAP principle
    - Consistency - is the data constant and correct through all servers in the system?
        - Eventual consistency - data that is not referenced often gets put in a place where it can be easily and quickly updated when necessary
    - Availability - is the data available?
    - Persistence - in case on server fails, another one can be used with no drop in performance
- Sharding (partition) - splitting data into multiple parts sent to different nodes so the system doesn’t rely on just one server
- Mapreduce - framework that maps a large amount of data and reduces them to their most important parts for communication.
- Schema-less db’s such as Cassandra or NoSQL enjoy faster performance because they rely only on key-value pairs.

# Sources

[A Thorough Introduction to Distributed Systems](https://www.freecodecamp.org/news/a-thorough-introduction-to-distributed-systems-3b91562c9b3c/)