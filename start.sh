#!/bin/bash
cd app
gunicorn app:app
