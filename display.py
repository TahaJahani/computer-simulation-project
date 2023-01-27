import math
import sys

import pygame
from pygame.rect import *
from job import Job, JOB_PRIORITY

QUEUE_PADDING = 4
QUEUE_MARGIN = 30
SIZE = WIDTH, HEIGHT = 1000, 550
JOB_SIZE = 30
JOB_MARGIN = 2
QUEUE_HEIGHT = JOB_SIZE + QUEUE_PADDING * 2
START_Y = 30
START_X = 20
sprites = []

priority_queue = {
    "name": "Priority: ",
    "x": START_X,
    "y": START_Y,
    "color": (0, 0, 92),
    "width": WIDTH - 2 * START_X,
    "height": QUEUE_HEIGHT
}

roundRobinT1_queue = {
    "name": "RR T1: ",
    "x": START_X,
    "y": QUEUE_HEIGHT + QUEUE_MARGIN + START_Y,
    "color": (59, 24, 95),
    "width": WIDTH - 2 * START_X,
    "height": QUEUE_HEIGHT
}

roundRobinT2_queue = {
    "name": "RR T2: ",
    "x": START_X,
    "y": 2 * (QUEUE_HEIGHT + QUEUE_MARGIN) + START_Y,
    "color": (192, 96, 161),
    "width": WIDTH - 2 * START_X,
    "height": QUEUE_HEIGHT
}

fcfs_queue = {
    "name": "FCFS: ",
    "x": START_X,
    "y": 3 * (QUEUE_HEIGHT + QUEUE_MARGIN) + START_Y,
    "color": (240, 202, 163),
    "width": WIDTH - 2 * START_X,
    "height": QUEUE_HEIGHT
}

this_module = sys.modules[__name__]
GRAY = (248, 237, 227)
screen = None
font = None
smaller_font = None
selected_job = None


def select_job(job: Job):
    global selected_job
    selected_job = job


def show_job_data():
    if selected_job is None:
        return
    y = 4 * (QUEUE_HEIGHT + QUEUE_MARGIN) + START_Y + 50
    margin = 30
    text = font.render(f"Job Data:", True, (0, 0, 0))
    screen.blit(text, (0, y))

    y += margin
    text = font.render(f"Job Id: {selected_job.id}", True, (0, 0, 0))
    screen.blit(text, (20, y))

    y += margin
    text = font.render(f"Creation Time: {selected_job.creation_time}", True, (0, 0, 0))
    screen.blit(text, (20, y))

    y += margin
    text = font.render(f"Service Time: {selected_job.service_time}", True, (0, 0, 0))
    screen.blit(text, (20, y))

    y += margin
    text = font.render(f"Executed Time: {selected_job.executed_time}", True, (0, 0, 0))
    screen.blit(text, (20, y))

    y += margin
    text = font.render(f"Priority: {selected_job.priority}", True, (0, 0, 0))
    screen.blit(text, (20, y))


def check_collision():
    for sprite in sprites:
        if sprite[1].collidepoint(pygame.mouse.get_pos()):
            return sprite[0]


def reset_screen():
    global sprites
    sprites = []
    screen.fill(GRAY)


def update_screen():
    pygame.display.update()


def initialize_display():
    global screen, font, smaller_font
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    font = pygame.font.Font('freesansbold.ttf', 16)
    smaller_font = pygame.font.Font('freesansbold.ttf', 12)


def get_job_priority_color(job: Job):
    if job.priority == 1:
        return 0, 132, 80
    if job.priority == 2:
        return 239, 183, 0
    if job.priority == 3:
        return 184, 29, 19


def get_job_rect(queue_rect, job: Job, index):
    queue = getattr(this_module, queue_rect)
    x = queue["x"] + QUEUE_PADDING + index * (JOB_SIZE + JOB_MARGIN)
    y = queue["y"] + QUEUE_PADDING
    done_percent = job.done_percent()
    if done_percent == 0:
        done_percent = 0.01
    rect = pygame.Rect((x, y), (JOB_SIZE, math.ceil(JOB_SIZE * done_percent)))
    outline = pygame.Rect((x, y), (JOB_SIZE, JOB_SIZE))
    pygame.draw.rect(screen, get_job_priority_color(job), rect, 0)
    pygame.draw.rect(screen, get_job_priority_color(job), outline, 2)
    job_id_text = smaller_font.render(f"{job.id}", True, (0, 0, 0), GRAY)
    screen.blit(job_id_text, (x + JOB_SIZE / 10, y + JOB_SIZE / 2))
    sprites.append((job.id, outline))


def get_queue_rects():
    queues = [priority_queue, roundRobinT1_queue, roundRobinT2_queue, fcfs_queue]
    for item in queues:
        rect = pygame.Rect((item["x"], item["y"]), (item["width"], item["height"]))
        pygame.draw.rect(screen, item["color"], rect, 2)
        text = font.render(item["name"], True, (0, 0, 0))
        screen.blit(text, (0, item["y"] - (QUEUE_MARGIN * 2 / 3)))


def show_text_data(current_time, next_job_time):
    y = 4 * (QUEUE_HEIGHT + QUEUE_MARGIN) + START_Y
    clock_text = font.render(f"Current Time: {current_time}", True, (0, 0, 0))
    job_text = font.render(f"Next Job Arrival: {next_job_time}", True, (0, 0, 0))
    screen.blit(clock_text, (0, y))
    screen.blit(job_text, (clock_text.get_rect().width + 100, y))
    show_job_data()
