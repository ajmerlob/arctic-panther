# arctic-panther
Creates optimal small-groups of data scientist

### This repo administers the Pair DS events.
1. Create weekly events (TODO - implement an API call)
2. Sends out survey reminders to people that are RSVP'd for an event, but that haven't take the survey.
3. Creates Pairs using a matching algorithm (TODO - improve this!!)
4. Sends out notifications to pairs.
5. Gives each participant a report about their pairing (TODO - write a report)

### Here's how it works:
- Core - Data models and simulators
  - User class - Container for user data
    - user_id from Meetup
    - gender, career stage, etc
    - self-reported geography (Likert class)
    - self-reported skills/tools/methods (Likert class)
    - preferences (Likert class)
  - Likert class - Dictionary holding lists holding survey data
  - Simulator class - Lets you test stuff out without real data
  - Config class - Holds configuration settings to access APIs, etc
- Pair - Pair data science
  - Main class - Drives the pair data science process
  - Analyze class - Container for analysis functions (called from Main)
  - Messages class - Sends messages from Meetup
  - Text class - Holds the text that's send in various messages
  - Parsers - Grabs data from various sources
    - APIParser - Grabs and parses data from SurveyMonkey API
    - TextParser - Grabs and parses data stored in text files
