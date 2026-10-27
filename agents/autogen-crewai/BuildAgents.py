# Now, let’s dive in to configure Autogen agents. But before that, set up the environment. 
# If the use case requires code execution, the agents will do it in the current environment, and as per the official documentation, 
# it is best done inside a container. To get started quickly, you can use GitHub codespaces. Make sure you install “pyautogen”.

# As of now, Autogen supports only OpenAI models. To effectively use agents, we need to configure our models.
# We can configure multiple OpenAI models and use the ones we need. 
# There are different ways to configure models, but we will define a JSON file.

# JSON file:


#OAI_CONFIG_LIST
[
    {
        "model": "gpt-4",
        "api_key": "<your OpenAI API key here>"
    },
    {
        "model": "gpt-4",
        "api_key": "<your Azure OpenAI API key here>",
        "base_url": "<your Azure OpenAI API base here>",
        "api_type": "azure",
        "api_version": "2023-07-01-preview"
    },
    {
        "model": "gpt-3.5-turbo",
        "api_key":  "<your OpenAI API key here>"
    }
]




# Now, define a config list for models.

import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": {
            "gpt-3.5-turbo"
        }
    }
)
# (This method will first search for OAI_CONFIG_LIST in the environment variable.
#  If unsuccessful, it will search for the OAI_CONFIG_LIST Json file in the current directory. 
#  The filter_dict is for filtering models based on some parameters, here it is set to model.)





# Configuration for LLM
# Now, we define the configuration for the LLM. 
# In this example, we will use a Jupyter Notebook function tool to run Python scripts to accomplish a simple graph plotting task.

llm_config = {
    "functions": [
        {
            "name": "python",
            "description": "run cell in ipython and return the execution result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cell": {
                        "type": "string",
                        "description": "Valid Python cell to execute.",
                    }
                },
                "required": ["cell"],
            },
        },
    ],
    "config_list": config_list,
    "timeout": 120,
}








