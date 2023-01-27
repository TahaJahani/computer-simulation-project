import math
import sys

import pygame
from pygame.rect import *
from job import Job, JOB_PRIORITY

QUEUE_PADDING = 4
QUEUE_MARGIN = 10
SIZE = WIDTH, HEIGHT = 1000, 400
JOB_SIZE = 30
JOB_MARGIN = 2
QUEUE_HEIGHT = JOB_SIZE + QUEUE_PADDING * 2

priority_queue = {
    "x": 5,
    "y": 5,
    "color": (0, 0, 92),
    "width": WIDTH - 10,
    "height": QUEUE_HEIGHT
}

roundRobinT1_queue = {
    "x": 5,
    "y": QUEUE_HEIGHT + 5 + QUEUE_MARGIN,
    "color": (59, 24, 95),
    "width": WIDTH - 10,
    "height": QUEUE_HEIGHT
}

roundRobinT2_queue = {
    "x": 5,
    "y": 2 * (QUEUE_HEIGHT + QUEUE_MARGIN) + 5,
    "color": (192, 96, 161),
    "width": WIDTH - 10,
    "height": QUEUE_HEIGHT
}

fcfs_queue = {
    "x": 5,
    "y": 3 * (QUEUE_HEIGHT + QUEUE_MARGIN) + 5,
    "color": (240, 202, 163),
    "width": WIDTH - 10,
    "height": QUEUE_HEIGHT
}

this_module = sys.modules[__name__]
GRAY = (248, 237, 227)
screen = None


def reset_screen():
    screen.fill(GRAY)


def update_screen():
    pygame.display.update()


def initialize_display():
    global screen
    pygame.init()
    screen = pygame.display.set_mode(SIZE)


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


def get_queue_rects():
    queues = [priority_queue, roundRobinT1_queue, roundRobinT2_queue, fcfs_queue]
    for item in queues:
        rect = pygame.Rect((item["x"], item["y"]), (item["width"], item["height"]))
        pygame.draw.rect(screen, item["color"], rect, 2)
