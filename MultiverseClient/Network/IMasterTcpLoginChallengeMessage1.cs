namespace Multiverse.Network
{
    public interface IMasterTcpLoginChallengeMessage1
    {
        byte[] Challenge { get; set; }
        int Version { get; set; }

        OutgoingMessage CreateMessage();
        bool Equals(object obj);
        int GetHashCode();
        string ToString();
    }
}