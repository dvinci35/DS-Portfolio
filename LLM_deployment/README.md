# Deploying an llm in Docker container

LLM is commonly being used and it has become necessary to learn how to deploy it in a Docker container. A docker image can be copied and run in any remote cloud machine with gpu machine with a very few number of steps.

Huggingface provides an inference api but it charges at hourly rates, but if you have a dedicated GPU laptop or cpu you can host your own inference api using container in your home/office network. The only charges are the power that the device will consume.

# Requirements

Here Qwen2 instruct model with 1.5 billion parameters is used for test deployment container. you can use any other model available on huggingface for text-generation task.

You can change the model in [config file](./app/config.yaml). These are the parameters of `pipeline` function specifically TextGenerationPipeline of transformers library - [link](https://huggingface.co/docs/transformers/main_classes/pipelines#transformers.TextGenerationPipeline)

Review the requirements file, add library name if you have other dependencies.

**Tested on python version: 3.10.x**

- Install the GPU drivers, if your machine has linux - Ubuntu, then following commands will suffice
  ```bash
  sudo apt-get update && sudo apt-get upgrade
  sudo apt-get install nvidia-drivers-535 nvidia-dkms-535 nvtop -y
  ```

- Nvidia container tool kit is needed to make the docker container utilize the system gpu: [official instructions](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) 

  FOR UBUNTU:
  ```bash
  curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

  sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list

  sudo apt-get update

  sudo apt-get install -y nvidia-container-toolkit

  sudo nvidia-ctk runtime configure --runtime=docker

  sudo systemctl restart docker
  ```

- Docker is needed (obviously) to run in a container. You can also create a server without containerization. Install docker official instructions
  FOR UBUNTU:
  ```bash
  for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done

  # Add Docker's official GPG key:
  sudo apt-get update
  sudo apt-get install ca-certificates curl
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc

  # Add the repository to Apt sources:
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update

  sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  ```

# Build and Run the container

Run the bash file [build_and_run.sh](build_and_run.sh)

```bash
docker build -t inf_api .

docker run \
    --runtime nvidia \
    --gpu all \
    -p 80:80 \
    inf_api
```

# Making Requests to the model

A simple client is written to get re

# Possible improvements

Huggingface inference API provides ways to handle large amount of queries and strategies to handle very long texts so that the deployment container does not break

- Find ways to handle infinite generation
- Is there a way for parallel response generation?
  
  The `transformers.pipeline` generates the word one at a time, so even if a list of input_text are given it will generated response for input one by one.
- Find specific ways to integrate it with IDEs like Visual Studio code
- Find ways to use it for simple tasks and use it on another device in private/home network.
- Is it possible to write a universal client module that can be used on any device?


---
*Feel free to use this as a reference and create your own version.*

*Any suggestions and feedbacks are welcome*

*If this repo helps you in any way hit the star :D*