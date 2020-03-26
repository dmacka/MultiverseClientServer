namespace Multiverse.Network
{
    public interface IMasterTcpLoginChallengeMessage
    {
        byte[] Challenge { get; set; }
        int Version { get; set; }

        OutgoingMessage CreateMessage();
        bool Equals(object obj);
        int GetHashCode();
        string ToString();
    }
}