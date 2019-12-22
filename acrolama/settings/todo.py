# Todo-specific settings
"""
Restrict access to ALL todo lists/views to `is_staff` users.
If False or unset, all users can see all views 
(but more granular permissions are still enforced
within views, such as requiring staff for adding and deleting lists).
"""
TODO_STAFF_ONLY = True

"""
If you use the "public" ticket filing option, to whom should these tickets be assigned?
Must be a valid username in your system. If unset, unassigned tickets go to "Anyone."
"""
TODO_DEFAULT_ASSIGNEE = "adrian@acrolama.com"

"""
If you use the "public" ticket filing option, to which list should these tickets be saved?
Defaults to first list found, which is probably not what you want!
"""
TODO_DEFAULT_LIST_SLUG = "tickets"
"""
If you use the "public" ticket filing option, to which *named URL* should the user be
redirected after submitting? (since they can't see the rest of the ticket system).
Defaults to "/"
"""
TODO_PUBLIC_SUBMIT_REDIRECT = "home"

"""
Enable or disable file attachments on Tasks
Optionally limit list of allowed filetypes
"""
TODO_ALLOW_FILE_ATTACHMENTS = False
TODO_ALLOWED_FILE_ATTACHMENTS = [".jpg", ".gif", ".csv", ".pdf", ".zip"]
TODO_MAXIMUM_ATTACHMENT_SIZE = 5000000  # In bytes

"""
additionnal classes the comment body should hold
adding "text-monospace" makes comment monospace
"""
TODO_COMMENT_CLASSES = []

"""
The following two settings are relevant only if you want todo to track a support mailbox -
see Mail Tracking below.
"""
# TODO_MAIL_BACKENDS
# TODO_MAIL_TRACKERS
