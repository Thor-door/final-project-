import argparse
import os

def loadTheList(fileName):
    taskList = []
    if os.path.exists(fileName):
        file = open(fileName, 'r')
        lines = file.readlines()
        file.close()

        for line in lines:
            task_info = line.strip().split(',')  
            if len(task_info) == 4:
                taskNumber = int(task_info[0])
                taskTopic = (task_info[1])
                taskDescription = (task_info[2])
                taskProgress = (task_info[3])
                taskList.append({
                    "Number": taskNumber,
                    "Topic": taskTopic,
                    "Description": taskDescription,
                    "Progress": taskProgress

                                })
    return taskList


def saveTheList(fileName, taskList):
    file = open(fileName, "w")
    for task in taskList:
        file.write(f"{task["Number"]},{task["Topic"]},{task["Description"]},{task["Progress"]} \n")
    file.close()

def displayTheList(taskList):
    if len(taskList) == 0:
        print("No tasks! (Yay?) ")
    else:
        for task in taskList:
            print("Number: " + str(task["Number"]) + "   ||| Topic: " + task["Topic"] + "   ||| Description: " + task["Description"] + "   ||| Progress: " + task["Progress"])

def addTask(fileName, taskTopic, taskDescription):
    taskList = loadTheList(fileName)

    taskNumber = 1
    for task in taskList:
        if task["Number"] >= taskNumber:
            taskNumber = task["Number"] + 1

    newTask = {
        "Number": taskNumber,
        "Topic": taskTopic,
        "Description": taskDescription,
        "Progress": "Not Started"
              }
    taskList.append(newTask)
    saveTheList(fileName, taskList)
    print(f"Task '{taskDescription}' added to the list!")

def changeProgress(fileName, taskNumber, newProgress):
    taskList = loadTheList(fileName)
    found = False
    for task in taskList:
        if task["Number"] == taskNumber:
            task["Progress"] = newProgress
            found = True
            break
    if not found:
        print(f"No task with the number {taskNumber} could be found!")
    else:
        saveTheList(fileName, taskList)
        print(f"Task number {taskNumber} progress has been changed to '{newProgress}' , well done!")

def editTask(fileName, taskNumber, newDescription=None, newTopic=None):
    taskList = loadTheList(fileName)
    found = False

    for task in taskList:
        if task["Number"] == taskNumber:
            if newDescription:
                task["Description"] = newDescription
            if newTopic:
                task["Topic"] = newTopic
            found = True
            break
        if not found:
            print(f"No task with the number {taskNumber} coukld be found!")
        else:
            saveTheList(fileName, taskList)
            print(f"Task number {taskNumber} has been updated!")

def main():
    parser = argparse.ArgumentParser(description="A To-do list tool.")
    parser.add_argument("--list-name", type=str, default="TODO.txt", help= "The name of the to-do list file. ")
    subparsers = parser.add_subparsers(dest = "command")
    subparsers.add_parser("List", help = "Displays current tasks")     

    addParser = subparsers.add_parser("Add", help = "Add a new task to the list")           
    addParser.add_argument("Topic", type = str, help = "Topic of the task, such as school, work, chores,")
    addParser.add_argument("Description", type=str, help="Description of the task")

    ProgressParser = subparsers.add_parser("ProgressChange", help = "Change the progress of a task")
    ProgressParser.add_argument("TaskNumber", type = int, help = "Task number")
    ProgressParser.add_argument("Progress", type=str, help = "Updated progreess of the task such as Not started, in Progress, Complete")

    editParser = subparsers.add_parser("Edit", help = "Editing a task's description, number, or topic")
    editParser.add_argument("TaskNumber", type = int, help = "Task number of the task you will edit")
    editParser.add_argument("Description", type=str, help="New description of the task")
    editParser.add_argument("Topic", type = str, help = "New topic for the task")

    args = parser.parse_args()
    taskList = loadTheList(args.list_name)

    if args.command == "List":
        displayTheList(taskList)
    elif args.command == "Add":
        addTask(args.list_name, args.Topic, args.Description)
    elif args.command == "Progress":
        changeProgress(args.list_name, args.TaskNumber, args.Progress)
    elif args.command == "Edit":
        editTask(args.list_name, args.TaskNumber, args.Description, args.Topic)
    
if __name__ == "__main__":
    main()