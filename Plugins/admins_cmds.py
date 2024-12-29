from datetime import datetime, timedelta
from telegram.ext import CommandHandler
from plugins.database import update_user, get_user, add_redeem_code
import random
import string

ADMIN_ID = "6035523795"  # Replace with your admin ID


def generate_code():
    """Generate a random redeem code."""
    return "GENAI-" + "-".join(
        "".join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(3)
    )


async def add_credits(update, context):
    """Add credits directly to a user."""
    if str(update.effective_user.id) != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("Usage: /add_credits <user_id> <amount>")
        return

    try:
        user_id = int(context.args[0])
        amount = int(context.args[1])

        user = get_user(user_id)
        user["credits"] += amount
        update_user(user_id, {"credits": user["credits"]})

        await update.message.reply_text(
            f"✅ Added {amount} credits to user {user_id}.\n💳 New Balance: {user['credits']}"
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid input. Ensure user ID and amount are numbers.")


async def remove_credits(update, context):
    """Remove credits directly from a user."""
    if str(update.effective_user.id) != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("Usage: /remove_credits <user_id> <amount>")
        return

    try:
        user_id = int(context.args[0])
        amount = int(context.args[1])

        user = get_user(user_id)
        if user["credits"] < amount:
            await update.message.reply_text("❌ User does not have enough credits.")
            return

        user["credits"] -= amount
        update_user(user_id, {"credits": user["credits"]})

        await update.message.reply_text(
            f"✅ Removed {amount} credits from user {user_id}.\n💳 New Balance: {user['credits']}"
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid input. Ensure user ID and amount are numbers.")


async def set_expiration(update, context):
    """Set user expiration."""
    if str(update.effective_user.id) != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("Usage: /set_expiration <user_id> <duration>")
        return

    try:
        user_id = int(context.args[0])
        duration = context.args[1]

        if duration.endswith("h"):
            new_expiration = datetime.now() + timedelta(hours=int(duration[:-1]))
        elif duration.endswith("d"):
            new_expiration = datetime.now() + timedelta(days=int(duration[:-1]))
        elif duration.endswith("mo"):
            new_expiration = datetime.now() + timedelta(days=int(duration[:-2]) * 30)
        else:
            await update.message.reply_text("❌ Invalid duration format. Use 'h', 'd', or 'mo'.")
            return

        update_user(user_id, {"expiration": new_expiration})

        await update.message.reply_text(
            f"✅ Set expiration for user {user_id} to {new_expiration.strftime('%Y-%m-%d %H:%M:%S')}."
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid input. Ensure user ID and duration are correct.")


async def generate_redeem(update, context):
    """Generate redeem codes."""
    if str(update.effective_user.id) != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    if len(context.args) < 3:
        await update.message.reply_text(
            "Usage: /generate_redeem <credits> <duration> <count>\n"
            "Example: /generate_redeem 50 1h 10"
        )
        return

    try:
        credits = int(context.args[0])
        duration = context.args[1]
        count = int(context.args[2])

        if duration.endswith("h"):
            expiration = datetime.now() + timedelta(hours=int(duration[:-1]))
            duration_display = f"{duration[:-1]} Hour(s)"
        elif duration.endswith("d"):
            expiration = datetime.now() + timedelta(days=int(duration[:-1]))
            duration_display = f"{duration[:-1]} Day(s)"
        elif duration.endswith("mo"):
            expiration = datetime.now() + timedelta(days=int(duration[:-2]) * 30)
            duration_display = f"{duration[:-2]} Month(s)"
        else:
            await update.message.reply_text("❌ Invalid duration format. Use 'h', 'd', or 'mo'.")
            return

        codes = [generate_code() for _ in range(count)]
        for code in codes:
            add_redeem_code(code, credits, expiration)

        message = "🔥 **GENAi Premium** 🔥\n\n"
        message += "Gift card codes are available:\n\n"
        for i, code in enumerate(codes, 1):
            message += f"  {i}. {code}\n"
        message += f"\n**Duration**: {duration_display}\n\n"
        message += "Type `/redeem <code>` in the chat.\n"
        message += "Enjoy your premium experience! 🎉"

        await update.message.reply_text(message, parse_mode="Markdown")
    except ValueError:
        await update.message.reply_text("❌ Invalid input. Ensure credits and count are numbers.")
