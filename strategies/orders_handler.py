async def get_orders(client, sandbox = True, **kwargs):
    if sandbox == False:
        return await client.orders.get_orders(**kwargs)
    else:
        return await client.sandbox.get_sandbox_orders(**kwargs)
        
async def get_portfolio(client, sandbox = True, **kwargs):
    if sandbox == False:
        return await client.operations.get_portfolio(**kwargs)
    else:
        return await client.sandbox.get_sandbox_portfolio(**kwargs)
        
async def get_accounts(client, sandbox = True):
    if sandbox == False:
        return await client.users.get_accounts()
    else:
        return await client.sandbox.get_sandbox_accounts()
        
async def post_order(client, sandbox = True, **kwargs):
    if sandbox == False:
        return await client.orders.post_order(**kwargs)
    else:
        return await client.sandbox.post_sandbox_order(**kwargs)
        
async def get_order_state(client, sandbox = True, **kwargs):
    if sandbox == False:
        return await client.orders.get_order_state(**kwargs)
    else:
        return await client.sandbox.get_sandbox_order_state(**kwargs)
