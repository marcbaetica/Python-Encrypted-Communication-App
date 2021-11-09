# Python-Encrypted-Communication-App

### Communication protocol:
///

### Technical implementation details:
- As a socket does not know the size of an incoming message, the other party will first forward a 10 byte character payload denoting this information.
  This packet is the size (in bytes) of how many characters the incoming message will contain.
  Its format is of a 10 digit numeric padded byte string, allowing for a maximum incoming payload just under 10 GB.
  For example: if the incoming message is of 324 bytes size, the received message will be 0000000324. 
- Similarly, every package has to be acknowledged prior to one party being allowed to send another message. The ACK package is: ...TBD

### Unexpected error handling:
- Message is not delivered. No ACK package has been received. A retry mechanism is in place.
- Network connection is broken. No mechanism is in place other than client attempting to re-connect.
  This will create a new server socket handler. No handling exists server side.

### TODOs:
- Chat UI (probably Kivy).
- Fix connection closing mechanism to rely only on empty message rather than keyword.
- Unexpected error handling scenarios.