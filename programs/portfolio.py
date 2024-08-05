from classes import CommandArgs, Portfolio, Position, SystemConfig

def buy(_: SystemConfig, portfolio: Portfolio, command_arguments: CommandArgs):
    """
    note to self
    buy expects arguments in the form:
    ticker, number of shares, cost per share
    
    """

    # error handling will be spruced up later

    # Not enough / too many args
    if len(command_arguments) != 3:
        return False  
    
    ticker, share_count, share_cost = command_arguments

    # Check argument types are as expected.
    try:
        # Generate position.
        new_position = Position(
            share_count=float(share_count),
            share_value=float(share_cost)
        )

    except ValueError:
        print("buy cli arg type wrong")
        return False
    
    # Add position to portfolio
    portfolio.buy_position(
        ticker_name=ticker,
        position=new_position
    )

    print(portfolio)
    print(portfolio.tickers.values())
    for it in portfolio.get_ticker(ticker).positions.values():
        print(it)
        print(repr(it))


def sell(_: SystemConfig, portfolio: Portfolio, command_arguments: CommandArgs):
    """
    note to self
    sell expects arguments in the form:
    ticker, number of shares, current price
    
    """

    # error handling will be spruced up later
    print(list(portfolio.tickers.values())[0])
    # Not enough / too many args
    if len(command_arguments) != 3:
        return False  
    
    ticker, share_count, share_cost = command_arguments

    # Check argument types are as expected.
    try:
        # Generate position.
        new_position = Position(
            share_count=float(share_count),
            share_value=float(share_cost),
            is_sell=True
        )

    except ValueError:
        print("buy cli arg type wrong")
        return False
    
    # Add position to portfolio
    portfolio.sell_position(
        ticker_name=ticker,
        position=new_position
    )

    print(portfolio)
    print(portfolio.tickers.values())
    for it in portfolio.get_ticker(ticker).positions.values():
        print(it)
        print(repr(it))
    print(list(portfolio.tickers.values())[0])

