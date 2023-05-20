class Node:
	def __init__(self, name, status, os, ip):
		self.name = name
		self.status = status
		self.os = os
		self.ip = ip

	def __str__(self):
		return f"Node name: {self.name}\nNode status: {self.status}\nNode IP: {self.ip}\nNode OS: {self.os}\n"
