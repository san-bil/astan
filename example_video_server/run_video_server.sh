#!/bin/bash

twistd -no web --path=$(dirname $0)/video_root --port=8080
