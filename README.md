# arctic-panther
Creates optimal small-groups of data scientist

### This repo administers the Pair DS events.
1. Create weekly events (TODO - implement an API call)
2. Sends out survey reminders to people that are RSVP'd for an event, but that haven't take the survey.
3. Creates Pairs using a matching algorithm (TODO - improve this!!)
4. Sends out notifications to pairs.
5. Gives each participant a report about their pairing (TODO - write a report)

### Here's how it works:
- Main class - Drives the process
- User class - Container for user data
  - user_id from Meetup
  - gender, career stage, etc
  - self-reported geography (Likert class)
  - self-reported skills/tools/methods (Likert class)
  - preferences (Likert class)
- Likert class - Dictionary holding lists 
- Analyze class - Container for analysis functions (called from Main)
