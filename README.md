LLM Document Assistant Application

# first we converting pdf pages to images beacuse pdf is unstructured data and we can lost meaning of data if we directly parse it
rq worker --url redis://valkey:6379 - command for running worker to execute jobs in queue in FIFO manner