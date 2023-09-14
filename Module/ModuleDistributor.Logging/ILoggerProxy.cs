using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ModuleDistributor.Logging
{
    public interface ILoggerProxy
    {
        ILogger Logger { get; }
    }
}
