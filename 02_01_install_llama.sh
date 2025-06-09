#!/bin/bash

# https://ollama.com/download/linux 

curl -fsSL https://ollama.com/install.sh | sh 

ollama serve

ollama run deepseek-r1:8b
