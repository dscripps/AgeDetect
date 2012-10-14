//
//  ViewController.m
//  AG02
//
//  Created by デービット スクリプス on 8/1/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "ViewController.h"
#import "DirectionsViewController.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad
{
    //save unique ID
    
    NSString *uuid = [[NSUserDefaults standardUserDefaults] stringForKey:@"uuid"];
    if (uuid == nil) {
        //create new uuid
        [[NSUserDefaults standardUserDefaults] setObject:[self createUUID] forKey:@"uuid"];
    }
    
    

    [super viewDidLoad];
    
	// Do any additional setup after loading the view, typically from a nib.
    hello.text = NSLocalizedString(@"Hi There!", @"");
    [startButton setTitle:NSLocalizedString(@"Proceed", @"") forState:UIControlStateNormal];
    [startButton setTitle:NSLocalizedString(@"Proceed", @"") forState:UIControlStateHighlighted];
    [startButton setTitle:NSLocalizedString(@"Proceed", @"") forState:UIControlStateDisabled];
    [startButton setTitle:NSLocalizedString(@"Proceed", @"") forState:UIControlStateSelected];
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}


// MARK: IBActions

// start button
- (IBAction)start:(id)sender
{
    
    DirectionsViewController *DirectionsView = [[DirectionsViewController alloc] initWithNibName:@"DirectionsViewController" bundle:nil];
    DirectionsView.modalTransitionStyle = UIModalTransitionStyleCrossDissolve;
    [self presentModalViewController:DirectionsView animated:YES];
    [self viewDidUnload];
    self = nil;
    //NSLog(@"START PRESSED!");
}

- (NSString *)createUUID
{
    CFUUIDRef theUUID = CFUUIDCreate(NULL);
    CFStringRef string = CFUUIDCreateString(NULL, theUUID);
    CFRelease(theUUID);
    return [(NSString *)string autorelease];
}


@end
