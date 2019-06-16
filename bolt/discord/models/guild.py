from bolt.discord.models.base import Enum, Model, Field, ListField, Snowflake, Timestamp
from bolt.discord.models.channel import Channel
from bolt.discord.models.user import User
from bolt.discord.permissions import Permission


class MessageNotificationLevel(Enum):
    ALL_MESSAGES = 0
    ONLY_MENTIONS = 1


class VerificationLevel(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


class ExplicitContentFilterLevel(Enum):
    DISABLED = 0
    MEMBERS_WITHOUT_ROLES = 1
    ALL_MEMBERS = 2


class MFALevel(Enum):
    NONE = 0
    ELEVATED = 1


class GuildMember(Model):
    __repr_keys__ = ['user']

    api = None

    user = Field(User)
    guild_id = Field(Snowflake)
    nick = Field(str)
    roles = ListField(int)
    joined_at = Field(Timestamp)
    deaf = Field(bool)
    mute = Field(bool)

    def __repr__(self):
        classname = f"{type(self).__name__}"
        return f"{classname}({repr(self.user)})"

    @property
    def mention(self):
        return f"<@{self.user.id}>"

    def squelch(self):
        self.api.modify_guild_member(self.guild_id, self.id, mute=True)

    def unsquelch(self):
        self.api.modify_guild_member(self.guild_id, self.id, mute=False)

    def deafen(self):
        self.api.modify_guild_member(self.guild_id, self.id, deaf=True)

    def undeafen(self):
        self.api.modify_guild_member(self.guild_id, self.id, deaf=False)

    def move(self, channel):
        self.api.modify_guild_member(self.guild_id, self.id, channel_id=channel.id)

    def whisper(self):
        raise NotImplementedError

    def kick(self, reason):
        raise NotImplementedError

    def ban(self, reason):
        raise NotImplementedError

    def unban(self, reason):
        raise NotImplementedError

    def set_nickname(self, nickname):
        raise NotImplementedError

    def add_role(self, role):
        self.api.add_guild_member_role(self.guild_id, self.id, role.id)

    def remove_role(self, role):
        self.api.remove_guild_member_role(self.guild_id, self.id, role.id)

    def has_role(self, role):
        return bool(self.roles.find(id=role.id))

    @property
    def id(self):
        return self.user.id


class Role(Model):
    __repr_keys__ = ['id', 'name']

    api = None

    id = Field(Snowflake, required=True)
    name = Field(str, required=True)
    color = Field(int)
    hoist = Field(bool)
    position = Field(int)
    permissions = Field(Permission)
    managed = Field(bool)
    mentionable = Field(bool)

    def delete(self):
        pass


class VoiceState(Model):
    guild_id = Field(Snowflake)
    channel_id = Field(Snowflake)
    user_id = Field(Snowflake)
    session_id = Field(str)
    deaf = Field(bool)
    mute = Field(bool)
    self_deaf = Field(bool)
    self_mute = Field(bool)
    suppress = Field(bool)


class ActivityType(Enum):
    GAME = 0
    STREAMING = 1
    LISTENING = 2


class Activity(Model):
    name = Field(str)
    type = Field(ActivityType)
    url = Field(str)
    application_id = Field(int)
    details = Field(str)
    state = Field(str)
    # timestamps:
    # party:
    # assets:


class Presence(Model):
    __repr_keys__ = ['user']

    user = Field(User)
    game = Field(Activity)
    guild_id = Field(Snowflake)
    status = Field(str)


class Ban(Model):
    reason = Field(str)
    user = Field(User)


class VoiceRegion(Model):
    id = Field(str)
    name = Field(str)
    vip = Field(bool)
    optimal = Field(bool)
    deprecated = Field(bool)
    custom = Field(bool)


class Emoji(Model):
    __repr_keys__ = ['id', 'name']

    id = Field(Snowflake, required=True)
    name = Field(str, required=True)
    roles = ListField(Role)
    user = ListField(User)
    require_colons = Field(bool, default=False)
    managed = Field(bool, default=False)
    animated = Field(bool, default=False)


class Guild(Model):
    __repr_keys__ = ['id', 'name']

    api = None

    id = Field(Snowflake, required=True)
    name = Field(str)
    icon = Field(str)
    splash = Field(str)
    owner = Field(bool, default=False)
    owner_id = Field(Snowflake)
    permissions = Field(Permission)
    region = Field(str)
    afk_channel_id = Field(Snowflake)
    afk_timeout = Field(int)
    embed_enabled = Field(bool, default=False)
    embed_channel_id = Field(Snowflake)
    verification_level = Field(VerificationLevel)
    default_message_notifications = Field(MessageNotificationLevel)
    explicit_content_filter = Field(ExplicitContentFilterLevel)
    roles = ListField(Role)
    emojis = ListField(Emoji)
    features = ListField(str)
    mfa_level = Field(MFALevel)
    application_id = Field(Snowflake)
    widget_enabled = Field(bool)
    widget_channel_id = Field(Snowflake)
    system_channel_id = Field(Snowflake)
    joined_at = Field(Timestamp)
    large = Field(bool)
    unavailable = Field(bool)
    member_count = Field(int)
    voice_states = ListField(VoiceState)
    members = ListField(GuildMember)
    channels = ListField(Channel)
    presences = ListField(Presence)

    def update(self):
        pass

    def delete(self):
        pass

    def leave(self):
        pass

    @property
    def system_channel(self):
        pass

    def get_owner(self):
        pass
