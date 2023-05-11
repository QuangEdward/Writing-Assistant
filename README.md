# Writing-Assistant


## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository:

   ```bash
   git clone https://github.com/QuangEdward/Writing-Assistant.git
   ```

3. Navigate into the project directory:

   ```bash
   $ cd Writing-Assistant
   ```

4. Create a new virtual environment:

   ```bash
   $ py -3 -m venv venv
   $ venv\Scripts\activate
   ```

5. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```
   
6. Fill OpenAI API key parameter at .env file:
    ```bash
   OPENAI_API_KEY= <API_KEY>
   ```
 
7. Run the app:

   ```bash
   $ flask run
   ```

You should now be able to access the app at [http://localhost:5000](http://localhost:5000)! 
