import docker

from telegram.ext import (
    ConversationHandler
)


class ContainerHandler:
    def __init__(self):
        self.docker_client = docker.from_env()


    async def container_list(self, update, context):
        # Get a list of docker container names currently running
        containers = [container.name for container in self.docker_client.containers.list()]
        reply_text = ''
        for i, container in enumerate(containers):
            reply_text += f'({i+1}) {container}\n'
        await update.message.reply_text(reply_text)
        return self.container_logs


    async def container_logs(self, update, context):
        if ' ' in update.message.text:
            container_index, tail_count = update.message.text.split()
        else:
            container_index, tail_count = update.message.text, 10

        container_index = int(container_index)
        tail_count = int(tail_count)

        containers = self.docker_client.containers.list()
        logs = containers[container_index-1].logs(tail=tail_count)
        
        # Send message with Markdown. \n is needed to properly send 1st line
        await update.message.reply_text(f'```\n{logs.decode("utf-8")}```', parse_mode='MarkdownV2')
        return ConversationHandler.END


    async def container_cancel(self, update, context):
        await update.message.reply_text('ok')
        return ConversationHandler.END
