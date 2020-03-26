namespace Multiverse.Network
{
    public interface IMasterTcpLoginAuthenticateMessage
    {
        byte[] Authenticator { get; set; }
    }
}