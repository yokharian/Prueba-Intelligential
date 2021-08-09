"""provides pytest imports full access to root directory"""
from os import environ
environ['IN_MEMORY_DATABASE'] = 'True'
