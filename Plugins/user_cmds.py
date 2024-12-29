from plugins.database import get_redeem_code, update_user, get_user


async def redeem(update, context):
    """Redeem a gift card code."""
    chat_id = update.effective_user.id
    user = get_user(chat_id)

    if len(context.args) < 1:
        await update.message.reply_text("Usage: /redeem <code>\nExample: /redeem GENAI-8APS-TM39-NVMN")
        return

    code = context.args[0].strip().upper()
    redeem_data = get_redeem_code(code)

    if not redeem_data:
        await update.message.reply_text("❌ Invalid or expired code. Please try again.")
        return

    credits_to_add = redeem_data["credits"]
    user["credits"] += credits_to_add

    if redeem_data["expiration"] > user["expiration"]:
        user["expiration"] = redeem_data["expiration"]
    update_user(chat_id, {"credits": user["credits"], "expiration": user["expiration"]})

    success_message = (
        f"🎉 **Redeemed Successfully!** 🎉\n\n"
        f"💳 **Credits Added**: {credits_to_add}\n"
        f"🕒 **New Expiration**: {user['expiration'].strftime('%Y-%m-%d')}\n\n"
        "Thank you for redeeming. Enjoy your premium experience!"
    )
    await update.message.reply_text(success_message, parse_mode="Markdown")
