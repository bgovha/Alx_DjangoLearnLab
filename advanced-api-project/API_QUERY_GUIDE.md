# Advanced API Query Guide

This guide explains how to use the filtering, searching, and ordering capabilities of the Book API.

## Overview

The Book API provides comprehensive query capabilities through URL parameters, allowing you to efficiently retrieve and manipulate data.

## Filtering

### Basic Filtering

Filter books by exact field matches:

```http
GET /api/books/?title=Harry Potter
GET /api/books/?author=1
GET /api/books/?publication_year=1997