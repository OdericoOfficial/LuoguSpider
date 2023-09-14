using Microsoft.EntityFrameworkCore;
using ModuleDistributor.EntityFrameworkCore;

namespace LuoguSpiderServer.EntityFrameworkCore
{
    public class SqliteOptionsWrapper : OptionsActionWrapper
    {
        public override Action<IServiceProvider, DbContextOptionsBuilder>? OptionsAction { get; }

        public SqliteOptionsWrapper()
            => OptionsAction = ConfigureDbContextOptions;

        private void ConfigureDbContextOptions(IServiceProvider services, DbContextOptionsBuilder options)
        {

        }
    }
}
