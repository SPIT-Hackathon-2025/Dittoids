# import os
# from datetime import datetime, timedelta
# import asyncio
# from dotenv import load_dotenv
# import logging
# from notion_client import Client
# from typing import Dict, Any, Optional

# # Set up logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# # class NotionManager:
# #     def __init__(self):
# #         """Initialize the Notion manager with environment variables"""
# #         load_dotenv()
        
# #         self.notion_api_key = os.getenv('NOTION_API_KEY')
# #         if not self.notion_api_key:
# #             raise ValueError("NOTION_API_KEY not found in .env file")
            
# #         self.notion = Client(auth=self.notion_api_key)
# #         self.database_id = None  # Will be set after database creation
        
# #     async def create_database(self, parent_page_id: str) -> str:
# #         """
# #         Create a new task management database in Notion
        
# #         Args:
# #             parent_page_id: The ID of the parent page where the database will be created
            
# #         Returns:
# #             str: The ID of the created database
# #         """
# #         try:
# #             logger.info("Creating new task management database...")
            
# #             # Define database schema
# #             database = self.notion.databases.create(
# #                 parent={"page_id": parent_page_id},
# #                 title=[{
# #                     "type": "text",
# #                     "text": {"content": "SP-TBI Task Management"}
# #                 }],
# #                 properties={
# #                     "Title": {"title": {}},
# #                     "Description": {"rich_text": {}},
# #                     "Status": {
# #                         "select": {
# #                             "options": [
# #                                 {"name": "Not Started", "color": "red"},
# #                                 {"name": "In Progress", "color": "yellow"},
# #                                 {"name": "Completed", "color": "green"},
# #                                 {"name": "On Hold", "color": "gray"}
# #                             ]
# #                         }
# #                     },
# #                     "Priority": {
# #                         "select": {
# #                             "options": [
# #                                 {"name": "High", "color": "red"},
# #                                 {"name": "Medium", "color": "yellow"},
# #                                 {"name": "Low", "color": "blue"}
# #                             ]
# #                         }
# #                     },
# #                     "Due Date": {"date": {}},
# #                     "Assignee": {"people": {}},
# #                     "Tags": {"multi_select": {
# #                         "options": [
# #                             {"name": "Meeting", "color": "blue"},
# #                             {"name": "Follow-up", "color": "green"},
# #                             {"name": "Administrative", "color": "orange"},
# #                             {"name": "Mentorship", "color": "purple"}
# #                         ]
# #                     }},
# #                     "Progress": {"number": {}}
# #                 }
# #             )
            
# #             self.database_id = database["id"]
# #             logger.info(f"Successfully created database with ID: {self.database_id}")
# #             return self.database_id
            
# #         except Exception as e:
# #             logger.error(f"Failed to create database: {str(e)}")
# #             raise
# class NotionManager:
#     async def create_database(self, parent_page_id: str) -> str:
#         """
#         Create a new task management database in Notion with enhanced error handling
        
#         Args:
#             parent_page_id: The ID of the parent page where the database will be created
            
#         Returns:
#             str: The ID of the created database
            
#         Raises:
#             ValueError: If the parent page ID is invalid
#             NotionValidationError: If the page is archived or has archived ancestors
#             NotionAuthenticationError: If API authentication fails
#         """
#         try:
#             # First verify the parent page exists and is accessible
#             try:
#                 parent_page = self.notion.pages.retrieve(page_id=parent_page_id)
                
#                 # Check if the page is archived
#                 if parent_page.get("archived", False):
#                     raise ValueError(f"Parent page {parent_page_id} is archived. Please unarchive it first.")
                    
#             except Exception as e:
#                 raise ValueError(f"Failed to access parent page: {str(e)}")
            
#             logger.info("Creating new task management database...")
            
#             # Define database schema
#             database = self.notion.databases.create(
#                 parent={"page_id": parent_page_id},
#                 title=[{
#                     "type": "text",
#                     "text": {"content": "SP-TBI Task Management"}
#                 }],
#                 properties={
#                     "Title": {"title": {}},
#                     "Description": {"rich_text": {}},
#                     "Status": {
#                         "select": {
#                             "options": [
#                                 {"name": "Not Started", "color": "red"},
#                                 {"name": "In Progress", "color": "yellow"},
#                                 {"name": "Completed", "color": "green"},
#                                 {"name": "On Hold", "color": "gray"}
#                             ]
#                         }
#                     },
#                     "Priority": {
#                         "select": {
#                             "options": [
#                                 {"name": "High", "color": "red"},
#                                 {"name": "Medium", "color": "yellow"},
#                                 {"name": "Low", "color": "blue"}
#                             ]
#                         }
#                     },
#                     "Due Date": {"date": {}},
#                     "Assignee": {"people": {}},
#                     "Tags": {"multi_select": {
#                         "options": [
#                             {"name": "Meeting", "color": "blue"},
#                             {"name": "Follow-up", "color": "green"},
#                             {"name": "Administrative", "color": "orange"},
#                             {"name": "Mentorship", "color": "purple"}
#                         ]
#                     }},
#                     "Progress": {"number": {}}
#                 }
#             )
            
#             self.database_id = database["id"]
#             logger.info(f"Successfully created database with ID: {self.database_id}")
#             return self.database_id
            
#         except Exception as e:
#             error_message = str(e)
#             if "archived ancestor" in error_message.lower():
#                 logger.error("Database creation failed: Parent page or its ancestors are archived")
#                 raise ValueError("Please check the parent page and its ancestors. Unarchive any archived pages in the hierarchy.")
#             elif "authentication" in error_message.lower():
#                 logger.error("Authentication failed: Please verify your Notion API key")
#                 raise ValueError("Invalid or expired Notion API key")
#             else:
#                 logger.error(f"Failed to create database: {error_message}")
#                 raise
#     async def create_task(self, task_data: Dict[str, Any]) -> Optional[str]:
#         """
#         Create a new task in the database
        
#         Args:
#             task_data: Dictionary containing task details
            
#         Returns:
#             Optional[str]: The ID of the created task, or None if creation failed
#         """
#         try:
#             if not self.database_id:
#                 raise ValueError("Database ID not set. Create or set database first.")
                
#             logger.info(f"Creating task: {task_data.get('title', 'Untitled')}")
            
#             # Prepare the properties dictionary
#             properties = {
#                 "Title": {
#                     "title": [{"text": {"content": task_data.get("title", "Untitled")}}]
#                 },
#                 "Description": {
#                     "rich_text": [{"text": {"content": task_data.get("description", "")}}]
#                 },
#                 "Status": {
#                     "select": {"name": task_data.get("status", "Not Started")}
#                 },
#                 "Priority": {
#                     "select": {"name": task_data.get("priority", "Medium")}
#                 }
#             }
            
#             # Add optional properties if provided
#             if "due_date" in task_data:
#                 properties["Due Date"] = {"date": {"start": task_data["due_date"]}}
            
#             if "tags" in task_data:
#                 properties["Tags"] = {"multi_select": [{"name": tag} for tag in task_data["tags"]]}
            
#             if "progress" in task_data:
#                 properties["Progress"] = {"number": task_data["progress"]}
            
#             # Create the task
#             new_task = self.notion.pages.create(
#                 parent={"database_id": self.database_id},
#                 properties=properties
#             )
            
#             logger.info(f"Successfully created task with ID: {new_task['id']}")
#             return new_task['id']
            
#         except Exception as e:
#             logger.error(f"Failed to create task: {str(e)}")
#             return None

#     async def update_task(self, task_id: str, updates: Dict[str, Any]) -> bool:
#         """
#         Update an existing task
        
#         Args:
#             task_id: The ID of the task to update
#             updates: Dictionary containing the fields to update
            
#         Returns:
#             bool: True if update was successful, False otherwise
#         """
#         try:
#             logger.info(f"Updating task: {task_id}")
            
#             # Prepare the properties dictionary
#             properties = {}
            
#             # Map the updates to Notion's property format
#             if "title" in updates:
#                 properties["Title"] = {"title": [{"text": {"content": updates["title"]}}]}
            
#             if "description" in updates:
#                 properties["Description"] = {"rich_text": [{"text": {"content": updates["description"]}}]}
            
#             if "status" in updates:
#                 properties["Status"] = {"select": {"name": updates["status"]}}
            
#             if "priority" in updates:
#                 properties["Priority"] = {"select": {"name": updates["priority"]}}
            
#             if "due_date" in updates:
#                 properties["Due Date"] = {"date": {"start": updates["due_date"]}}
            
#             if "tags" in updates:
#                 properties["Tags"] = {"multi_select": [{"name": tag} for tag in updates["tags"]]}
            
#             if "progress" in updates:
#                 properties["Progress"] = {"number": updates["progress"]}
            
#             # Update the task
#             self.notion.pages.update(
#                 page_id=task_id,
#                 properties=properties
#             )
            
#             logger.info(f"Successfully updated task: {task_id}")
#             return True
            
#         except Exception as e:
#             logger.error(f"Failed to update task: {str(e)}")
#             return False

#     async def query_tasks(self, filters: Optional[Dict[str, Any]] = None) -> list:
#         """
#         Query tasks from the database with optional filters
        
#         Args:
#             filters: Dictionary containing filter criteria
            
#         Returns:
#             list: List of tasks matching the criteria
#         """
#         try:
#             if not self.database_id:
#                 raise ValueError("Database ID not set. Create or set database first.")
            
#             logger.info("Querying tasks...")
            
#             # Prepare filter conditions if provided
#             filter_conditions = {}
#             if filters:
#                 if "status" in filters:
#                     filter_conditions["property"] = "Status"
#                     filter_conditions["select"] = {"equals": filters["status"]}
#                 # Add more filter conditions as needed
            
#             # Query the database
#             response = self.notion.databases.query(
#                 database_id=self.database_id,
#                 filter=filter_conditions if filter_conditions else None
#             )
            
#             logger.info(f"Successfully retrieved {len(response['results'])} tasks")
#             return response['results']
            
#         except Exception as e:
#             logger.error(f"Failed to query tasks: {str(e)}")
#             return []

# async def main():
#     """Example usage of the NotionManager class"""
#     try:
#         # Create manager instance
#         manager = NotionManager()
        
#         # Create new database (replace with your parent page ID)
#         parent_page_id = os.getenv('NOTION_PAGE_ID')
#         await manager.create_database(parent_page_id)
        
#         # Create a sample task
#         task_data = {
#             "title": "Review Startup Applications",
#             "description": "Review and evaluate new startup applications for the incubation program",
#             "status": "Not Started",
#             "priority": "High",
#             "due_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
#             "tags": ["Administrative", "Mentorship"],
#             "progress": 0
#         }
        
#         task_id = await manager.create_task(task_data)
        
#         if task_id:
#             # Update the task
#             updates = {
#                 "status": "In Progress",
#                 "progress": 25
#             }
#             await manager.update_task(task_id, updates)
            
#             # Query tasks
#             tasks = await manager.query_tasks({"status": "In Progress"})
#             for task in tasks:
#                 logger.info(f"Task: {task['properties']['Title']['title'][0]['text']['content']}")
        
#         logger.info("All operations completed successfully!")
        
#     except Exception as e:
#         logger.error(f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     asyncio.run(main())
import os
from datetime import datetime, timedelta
import asyncio
from dotenv import load_dotenv
import logging
from notion_client import Client
from typing import Dict, Any, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NotionManager:
    def __init__(self):
        """Initialize the Notion manager with environment variables"""
        load_dotenv()
        
        self.notion_api_key = os.getenv('NOTION_API_KEY')
        if not self.notion_api_key:
            raise ValueError("NOTION_API_KEY not found in .env file")
            
        self.notion = Client(auth=self.notion_api_key)
        self.database_id = None  # Will be set after database creation
        
    async def create_database(self, parent_page_id: str) -> str:
        """
        Create a new task management database in Notion with enhanced error handling
        
        Args:
            parent_page_id: The ID of the parent page where the database will be created
            
        Returns:
            str: The ID of the created database
            
        Raises:
            ValueError: If the parent page ID is invalid
            NotionValidationError: If the page is archived or has archived ancestors
            NotionAuthenticationError: If API authentication fails
        """
        try:
            # First verify the parent page exists and is accessible
            try:
                parent_page = self.notion.pages.retrieve(page_id=parent_page_id)
                
                # Check if the page is archived
                if parent_page.get("archived", False):
                    raise ValueError(f"Parent page {parent_page_id} is archived. Please unarchive it first.")
                    
            except Exception as e:
                raise ValueError(f"Failed to access parent page: {str(e)}")
            
            logger.info("Creating new task management database...")
            
            # Define database schema
            database = self.notion.databases.create(
                parent={"page_id": parent_page_id},
                title=[{
                    "type": "text",
                    "text": {"content": "SP-TBI Task Management"}
                }],
                properties={
                    "Title": {"title": {}},
                    "Description": {"rich_text": {}},
                    "Status": {
                        "select": {
                            "options": [
                                {"name": "Not Started", "color": "red"},
                                {"name": "In Progress", "color": "yellow"},
                                {"name": "Completed", "color": "green"},
                                {"name": "On Hold", "color": "gray"}
                            ]
                        }
                    },
                    "Priority": {
                        "select": {
                            "options": [
                                {"name": "High", "color": "red"},
                                {"name": "Medium", "color": "yellow"},
                                {"name": "Low", "color": "blue"}
                            ]
                        }
                    },
                    "Due Date": {"date": {}},
                    "Assignee": {"people": {}},
                    "Tags": {"multi_select": {
                        "options": [
                            {"name": "Meeting", "color": "blue"},
                            {"name": "Follow-up", "color": "green"},
                            {"name": "Administrative", "color": "orange"},
                            {"name": "Mentorship", "color": "purple"}
                        ]
                    }},
                    "Progress": {"number": {}}
                }
            )
            
            self.database_id = database["id"]
            logger.info(f"Successfully created database with ID: {self.database_id}")
            return self.database_id
            
        except Exception as e:
            error_message = str(e)
            if "archived ancestor" in error_message.lower():
                logger.error("Database creation failed: Parent page or its ancestors are archived")
                raise ValueError("Please check the parent page and its ancestors. Unarchive any archived pages in the hierarchy.")
            elif "authentication" in error_message.lower():
                logger.error("Authentication failed: Please verify your Notion API key")
                raise ValueError("Invalid or expired Notion API key")
            else:
                logger.error(f"Failed to create database: {error_message}")
                raise

    async def create_task(self, task_data: Dict[str, Any]) -> Optional[str]:
        """
        Create a new task in the database
        
        Args:
            task_data: Dictionary containing task details
            
        Returns:
            Optional[str]: The ID of the created task, or None if creation failed
        """
        try:
            if not self.database_id:
                raise ValueError("Database ID not set. Create or set database first.")
                
            logger.info(f"Creating task: {task_data.get('title', 'Untitled')}")
            
            # Prepare the properties dictionary
            properties = {
                "Title": {
                    "title": [{"text": {"content": task_data.get("title", "Untitled")}}]
                },
                "Description": {
                    "rich_text": [{"text": {"content": task_data.get("description", "")}}]
                },
                "Status": {
                    "select": {"name": task_data.get("status", "Not Started")}
                },
                "Priority": {
                    "select": {"name": task_data.get("priority", "Medium")}
                }
            }
            
            # Add optional properties if provided
            if "due_date" in task_data:
                properties["Due Date"] = {"date": {"start": task_data["due_date"]}}
            
            if "tags" in task_data:
                properties["Tags"] = {"multi_select": [{"name": tag} for tag in task_data["tags"]]}
            
            if "progress" in task_data:
                properties["Progress"] = {"number": task_data["progress"]}
            
            # Create the task
            new_task = self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )
            
            logger.info(f"Successfully created task with ID: {new_task['id']}")
            return new_task['id']
            
        except Exception as e:
            logger.error(f"Failed to create task: {str(e)}")
            return None

    async def update_task(self, task_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update an existing task
        
        Args:
            task_id: The ID of the task to update
            updates: Dictionary containing the fields to update
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            logger.info(f"Updating task: {task_id}")
            
            # Prepare the properties dictionary
            properties = {}
            
            # Map the updates to Notion's property format
            if "title" in updates:
                properties["Title"] = {"title": [{"text": {"content": updates["title"]}}]}
            
            if "description" in updates:
                properties["Description"] = {"rich_text": [{"text": {"content": updates["description"]}}]}
            
            if "status" in updates:
                properties["Status"] = {"select": {"name": updates["status"]}}
            
            if "priority" in updates:
                properties["Priority"] = {"select": {"name": updates["priority"]}}
            
            if "due_date" in updates:
                properties["Due Date"] = {"date": {"start": updates["due_date"]}}
            
            if "tags" in updates:
                properties["Tags"] = {"multi_select": [{"name": tag} for tag in updates["tags"]]}
            
            if "progress" in updates:
                properties["Progress"] = {"number": updates["progress"]}
            
            # Update the task
            self.notion.pages.update(
                page_id=task_id,
                properties=properties
            )
            
            logger.info(f"Successfully updated task: {task_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update task: {str(e)}")
            return False

    async def query_tasks(self, filters: Optional[Dict[str, Any]] = None) -> list:
        """
        Query tasks from the database with optional filters
        
        Args:
            filters: Dictionary containing filter criteria
            
        Returns:
            list: List of tasks matching the criteria
        """
        try:
            if not self.database_id:
                raise ValueError("Database ID not set. Create or set database first.")
            
            logger.info("Querying tasks...")
            
            # Prepare filter conditions if provided
            filter_conditions = {}
            if filters:
                if "status" in filters:
                    filter_conditions["property"] = "Status"
                    filter_conditions["select"] = {"equals": filters["status"]}
                # Add more filter conditions as needed
            
            # Query the database
            response = self.notion.databases.query(
                database_id=self.database_id,
                filter=filter_conditions if filter_conditions else None
            )
            
            logger.info(f"Successfully retrieved {len(response['results'])} tasks")
            return response['results']
            
        except Exception as e:
            logger.error(f"Failed to query tasks: {str(e)}")
            return []

async def main():
    """Example usage of the NotionManager class"""
    try:
        # Create manager instance
        manager = NotionManager()
        
        # Create new database (replace with your parent page ID)
        parent_page_id = os.getenv('NOTION_PAGE_ID')
        await manager.create_database(parent_page_id)
        
        # Create a sample task
        task_data = {
            "title": "Review Startup Applications",
            "description": "Review and evaluate new startup applications for the incubation program",
            "status": "Not Started",
            "priority": "High",
            "due_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "tags": ["Administrative", "Mentorship"],
            "progress": 0
        }
        
        task_id = await manager.create_task(task_data)
        
        if task_id:
            # Update the task
            updates = {
                "status": "In Progress",
                "progress": 25
            }
            await manager.update_task(task_id, updates)
            
            # Query tasks
            tasks = await manager.query_tasks({"status": "In Progress"})
            for task in tasks:
                logger.info(f"Task: {task['properties']['Title']['title'][0]['text']['content']}")
        
        logger.info("All operations completed successfully!")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())